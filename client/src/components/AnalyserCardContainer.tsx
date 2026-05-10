import { useEffect, useRef, useState } from "react"
import AnalyserCard from "../components/AnalyserCard"

const cards = [
  { name: "PyLint", level: 1 },
  { name: "Flake8", level: 3 },
  { name: "ESLint", level: 5 },
  { name: "Complexity", level: 3 },
  { name: "Security", level: 1 },
]

export default function AnalyserCardCotainer()
{
  const containerRef = useRef<HTMLDivElement>(null)
  const [visibleCount, setVisibleCount] = useState(cards.length)

  useEffect(() => {
    const update = () => {
      const container = containerRef.current
      if (!container) return

      const containerWidth = container.offsetWidth
      const cardWidth = 144 + 8 // w-36 + gap-2

      const maxFit = Math.floor(containerWidth / cardWidth)
      setVisibleCount(maxFit)
    }

    update()
    window.addEventListener("resize", update)
    return () => window.removeEventListener("resize", update)
  }, [])

  const visibleCards = (() => {
    const total = cards.length
    if (visibleCount >= total) return cards

    const cardsToRender = (total - visibleCount) / 2
    const start = Math.ceil(cardsToRender)
    const end = Math.floor(cardsToRender) + visibleCount
    return cards.slice(start, end)
  })()

  return (
    <div
      ref={containerRef}
      className="flex flex-row justify-center items-center w-full gap-2 overflow-hidden p-5"
    >
      {visibleCards.map((c, i) => (
        <AnalyserCard key={i} {...c} />
      ))}
    </div>
  )
}
