import AnalyserCardCotainer from "../components/AnalyserCardContainer"

export default function Landing()
{
  return (
    <main className="h-screen flex flex-col justify-start items-center p-10">
        <div className="w-full xl:w-7xl p-6">
            <h1 className="text-5xl text-left">
                LintSlayer
            </h1>
        </div>
        <AnalyserCardCotainer/>
        <div className="xl:w-7xl m-4 flex flex-col gap-4">
            <p className="">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua
            </p>
            <p className="">
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </p>
        </div>
    </main>
  )
}
