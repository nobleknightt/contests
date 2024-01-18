import { useEffect, useState } from 'react'


function formatDate(isoFormatStr) {
  const date = new Date(isoFormatStr)
  const options = {
    hour12: true, weekday: "short", year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"
  }
  return date.toLocaleString(navigator.language, options).replace('am', 'AM').replace('pm', 'PM')
}

function formatDuration(durationSeconds) {
  const minutes = durationSeconds / 60
  return `${(minutes / 60).toFixed()}:${(minutes % 60).toString().padStart(2, "0")}`
}

function Card({ platform, title, url, startTime, duration, isVisible }) {
  return (
    <div className={`${isVisible ? 'flex' : 'hidden'} flex-col border px-2 py-1 w-full`}>
      <div>{platform}</div>
      <div className="text-xl text-wrap"><a href={url}>{title}</a></div>
      <div className="flex gap-2">
        <div className="border p-1">{formatDate(startTime)}</div>
        <div className="border p-1">{formatDuration(duration)}</div>
      </div>
    </div>
  )
}

function App() {
  const [contests, setContests] = useState([])
  const platforms = ["AtCoder", "CodeChef", "Codeforces", "GeeksforGeeks", "HackerEarth", "LeetCode"]
  const [selectedPlatforms, setSelectedPlatforms] = useState({})
  const url = import.meta.env.VITE_API_URL

  useEffect(() => {
    setSelectedPlatforms(
      platforms.reduce((_selectedPlatforms, platform) => {
          return {..._selectedPlatforms, [platform]: true,
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
    <div className="flex flex-col h-screen">
      <div className="flex flex-wrap w-full items-center justify-center font-['Atkinson_Hyperlegible'] p-1 gap-1">
        {
          platforms.map(platform => (
            <div
              key={platform.toLowerCase()}
              className={`border px-2 py-1 hover:cursor-pointer ${selectedPlatforms[platform]
                  ? 'bg-green-400'
                  : 'bg-white'
                }`}
              onClick={() => setSelectedPlatforms({
                ...selectedPlatforms, [platform]: !selectedPlatforms[platform]
              })}
            >{platform}</div>
          ))
        }
      </div>
      <div className="grow overflow-auto flex flex-col w-fit mx-auto font-['Atkinson_Hyperlegible'] p-1 gap-1">
        {
          contests.map(contest => (
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
