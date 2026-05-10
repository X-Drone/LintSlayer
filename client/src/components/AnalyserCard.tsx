interface AnalyserCardProps
{
    name: string
    level: number
}

const heightMap: Record<number, string> = {
  1: 'h-24',
  2: 'h-32',
  3: 'h-40',
  4: 'h-48',
  5: 'h-56',
}

export default function AnalyserCard({name, level}: AnalyserCardProps)
{
  const height = heightMap[level] ?? 'h-20'
  return (
    <div className={`
      w-36 ${height} p-3 shrink-0
      bg-linear-to-br from-blue-400 to-blue-600
      dark:from-blue-600 dark:to-blue-800
      rounded-xl
      shadow-lg shadow-black/20
      flex flex-col justify-center
      transition-all duration-300
      hover:scale-105 hover:shadow-xl
    `}>
        <h5 className="text-lg text-center truncate">
            {name}
        </h5>
    </div>
  )
}
