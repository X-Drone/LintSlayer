interface AnalyserCardProps
{
    name: string
    level: number
}

const heightMap: Record<number, string> = {
  1: 'h-16',
  2: 'h-20',
  3: 'h-24',
  4: 'h-28',
  5: 'h-32',
}

export default function AnalyserCard({name, level}: AnalyserCardProps)
{
  const height = heightMap[level] ?? 'h-20'
  return (
    <div className={`w-36 ${height} p-3 shrink-0 bg-blue-400 dark:bg-blue-600 shadow-cyan-950 shadow-md flex flex-col justify-center overflow-hidden`}>
        <h5 className="text-lg text-center truncate">
            {name}
        </h5>
    </div>
  )
}
