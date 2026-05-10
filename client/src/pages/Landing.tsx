import AnalyserCardCotainer from "../components/AnalyserCardContainer"

export default function Landing()
{
  return (
    <div className="min-h-screen flex flex-col items-center px-6 py-16 gap-16">

    {/* HERO */}
        <section className="w-full max-w-5xl">
            <h1 className="text-6xl xl:text-7xl font-semibold tracking-tight text-shadow-2xs text-shadow-gray-900 dark:text-shadow-gray-400">
                LintSlayer
            </h1>
            <p className="text-xl text-neutral-600 dark:text-neutral-400 max-w-2xl mt-4">
                Hunt down code issues before they hunt you.
            </p>
        </section>

    {/* ANALYSERS */}
        <section className="w-full max-w-5xl">
            <AnalyserCardCotainer/>
        </section>

    {/* DESCRIPTION */}
        <section className="w-full max-w-4xl flex flex-col gap-4 text-neutral-700 dark:text-neutral-300">
            <p>
                Powerful static analysis unified into one workflow.
            </p>
            <p>
                See problems before they become bugs. Optimize before it hurts.
            </p>
        </section>
    </div>
  )
}
