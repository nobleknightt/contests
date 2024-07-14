import { useEffect, useState } from "react"
import Card from "./components/Card"
import { compareDates, platformIcons } from "./utils"
import clear from "./assets/clear.png"
import github from "./assets/github.png"


function App() {
  const [contests, setContests] = useState([])
  const [selectedPlatforms, setSelectedPlatforms] = useState({})

  const platforms = ["AtCoder", "CodeChef", "Codeforces", "GeeksforGeeks", "LeetCode"]

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
        <div className="border pl-1 pr-2 mb-2 h-8 inline-flex items-center text-xl tracking-tighter decoration-1 decoration-gray-200 underline hover:decoration-gray-950 hover:border-gray-950">
          <img src={github} width={24} height={24}></img>
          <a href="https://github.com/nobleknightt/contests" target="_blank">GitHub</a>
        </div>
      </div>
      <div className="flex flex-wrap w-full items-center justify-center p-1 mb-2 gap-1">
        {
          platforms.map(platform => (
            <div
              key={platform.toLowerCase()}
              className={`flex gap-2 border px-2 py-1 hover:cursor-pointer hover:border-gray-950 ${selectedPlatforms[platform]
                ? 'bg-blue-200'
                : 'bg-white'
                }`}
              onClick={() => setSelectedPlatforms({
                ...selectedPlatforms, [platform]: !selectedPlatforms[platform]
              })}
            >
              <img src={platformIcons[platform]} width={24} height={24}></img>
              {platform}
            </div>
          ))
        }
        <div
          className={`flex items-center justify-center gap-1 border pl-1 pr-2 py-1 hover:cursor-pointer hover:border-gray-950 ${Object.values(selectedPlatforms).filter((value) => value).length > 0
            ? 'bg-blue-200'
            : 'bg-white'
            }`}
          onClick={() => {
            setSelectedPlatforms(
              platforms.reduce((_selectedPlatforms, platform) => {
                return {
                  ..._selectedPlatforms, [platform]: false,
                }
              }, {})
            )
          }}
        ><img src={clear} width={24} height={24} className="p-1"></img>Clear</div>
      </div>
      <div className="grow overflow-auto flex flex-col w-fit px-1 gap-1 md:w-[752px]">
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
      <div className="pt-1">
        <p className="inline-flex items-center justify-center gap-1 flex-wrap">
          Built with <img src="https://img.icons8.com/?size=100&id=123603&format=png&color=000000" width={16} height={16} className="inline"></img> React, <img src="https://img.icons8.com/?size=100&id=CIAZz2CYc6Kc&format=png&color=000000" width={16} height={16} className="inline"></img> Tailwind and <img src="https://img.icons8.com/?size=100&id=Mjt9Tkm04cgv&format=png&color=000000" width={16} height={16} className="inline"></img> Love.
        </p>
      </div>
    </div>
  )
}

export default App
