import AnalyserCard from "../components/AnalyserCard"

export default function AnalyserCardCotainer()
{
  return (
    <div className="p-2 flex flex-row justify-center items-center w-full overflow-x-hidden gap-2">
        <AnalyserCard name="PyLint" level={1}/>
        <AnalyserCard name="Flake8" level={3}/>
        <AnalyserCard name="ESLint" level={5}/>
        <AnalyserCard name="Complexity" level={3}/>
        <AnalyserCard name="Security" level={1}/>
    </div>
  )
}
