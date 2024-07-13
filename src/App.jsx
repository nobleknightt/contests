import { useEffect, useState } from "react"
import Card from "./components/Card"
import { compareDates } from "./utils"

function App() {
  const [contests, setContests] = useState([])
  const platforms = ["AtCoder", "CodeChef", "Codeforces", "GeeksforGeeks", "LeetCode"]
  const [selectedPlatforms, setSelectedPlatforms] = useState({})
  const url = import.meta.env.VITE_API_URL

  useEffect(() => {
    setSelectedPlatforms(
      platforms.reduce((_selectedPlatforms, platform) => {
        return {
          ..._selectedPlatforms, [platform]: true,
        }
      }, {})
    )
    fetch(url).then(
      response => response.json()
    ).then(
      response => setContests(response)
    )
  }, [])

  return (
    <div className="tracking-tight font-['Atkinson_Hyperlegible'] flex flex-col items-center h-screen px-1 py-2">
      <div className="flex px-2 items-end justify-center flex-wrap gap-2">
        <div className="text-6xl tracking-tighter">Contests</div>
        <div className="border p-2 mb-2 h-8 inline-flex items-center text-xl tracking-tighter decoration-1 decoration-gray-200 underline hover:decoration-gray-950 hover:border-gray-950">
          <a href="https://github.com/er-knight/contests">GitHub</a>
        </div>
      </div>
      <div className="p-1 text-center">
        <span>Built with </span>
        <a href="https://github.com/er-knight/contests/tree/main/app/src/App.jsx" className="decoration-1 decoration-gray-200 underline hover:decoration-gray-950">React</a>
        <span> and </span>
        <a href="https://github.com/er-knight/contests/tree/main/app/src/App.jsx" className="decoration-1 decoration-gray-200 underline hover:decoration-gray-950">Tailwind CSS</a>
        <span> with little help from </span>
        <a href="https://github.com/er-knight/contestsdb" className="decoration-1 decoration-gray-200 underline hover:decoration-gray-950">Python</a>
      </div>
      <div className="flex flex-wrap w-full items-center justify-center p-1 mb-2 gap-1">
        {
          platforms.map(platform => (
            <div
              key={platform.toLowerCase()}
              className={`border px-2 py-1 hover:cursor-pointer hover:border-gray-950 ${selectedPlatforms[platform]
                ? 'bg-blue-200'
                : 'bg-white'
                }`}
              onClick={() => setSelectedPlatforms({
                ...selectedPlatforms, [platform]: !selectedPlatforms[platform]
              })}
            >{platform}</div>
          ))
        }
      </div>
      <div className="grow overflow-auto flex flex-col w-fit  px-1 gap-1 md:w-[752px]">
        {
          [].concat(contests).sort(
            (a, b) => compareDates(a.start_time, b.start_time)
          ).map(contest => (
            <Card
              key={contest.id}
              platform={contest.platform}
              title={contest.title}
              url={contest.url}
              startTime={contest.start_time}
              duration={contest.duration}
              isVisible={selectedPlatforms[contest.platform]}
            ></Card>
          ))
        }
      </div>
    </div>
  )
}

export default App
