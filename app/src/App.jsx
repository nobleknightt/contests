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

function compareDates(first, second) {
  const firstDate = new Date(first)
  const secondDate = new Date(second)
  console.log(firstDate, secondDate, firstDate - secondDate)
  return firstDate - secondDate
}

function Card({ platform, title, url, startTime, duration, isVisible }) {
  return (
    <div className={`${isVisible ? 'flex' : 'hidden'} flex-col border px-2 py-1 w-full hover:border-gray-950`}>
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
    <div className="tracking-tight font-['Atkinson_Hyperlegible'] flex flex-col items-center h-screen">
      <div className="flex p-2 items-end gap-4">
        <div className="text-6xl tracking-tighter">Contests</div>
        <div className="border p-2 mb-2 h-8 inline-flex items-center text-xl tracking-tighter decoration-1 decoration-gray-200 underline hover:decoration-gray-950 hover:border-gray-950">
          <a href="https://github.com/er-knight/contests">GitHub</a>
        </div>
      </div>
      <div className="p-2 pt-0 text-center">Built with 
        <a href="https://github.com/er-knight/contests/tree/main/app/src/App.jsx" className="pl-1 decoration-1 decoration-gray-200 underline hover:decoration-gray-950">React</a> and 
        <a href="https://github.com/er-knight/contests/tree/main/app/src/App.jsx" className="pl-1 decoration-1 decoration-gray-200 underline hover:decoration-gray-950">Tailwind CSS</a> with little help from 
        <a href="https://github.com/er-knight/contests/blob/main/update-contests.py" className="pl-1 decoration-1 decoration-gray-200 underline hover:decoration-gray-950">Python</a>
      </div>
      <div className="flex flex-wrap w-full items-center justify-center p-1 gap-1">
        {
          platforms.map(platform => (
            <div
              key={platform.toLowerCase()}
              className={`border px-2 py-1 hover:cursor-pointer hover:border-gray-950 ${selectedPlatforms[platform]
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
      <div className="grow overflow-auto flex flex-col w-fit mx-auto p-1 gap-1 md:w-[768px]">
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
