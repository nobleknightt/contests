import AtCoder from "../assets/atcoder.png"
import CodeChef from "../assets/codechef.png"
import Codeforces from "../assets/codeforces.png"
import GeeksforGeeks from "../assets/geeksforgeeks.png"
import LeetCode from "../assets/leetcode.png"

function formatDate(isoFormatStr) {
    const date = new Date(isoFormatStr)
    let options = {
        hour12: true, hour: "numeric", minute: "2-digit"
    }
    const today = new Date()
    if (date.toDateString() === today.toDateString()) {
        return `Today, ${date.toLocaleTimeString(navigator.language, options).replace('am', 'AM').replace('pm', 'PM')}`
    }
    const yesterday = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1)
    if (date.toDateString() === yesterday.toDateString()) {
        return `Yesterday, ${date.toLocaleTimeString(navigator.language, options).replace('am', 'AM').replace('pm', 'PM')}`
    }
    const tomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1)
    if (date.toDateString() === tomorrow.toDateString()) {
        return `Tomorrow, ${date.toLocaleTimeString(navigator.language, options).replace('am', 'AM').replace('pm', 'PM')}`
    }
    options = { ...options, weekday: "short", year: "numeric", month: "short", day: "numeric" }
    return date.toLocaleString(navigator.language, options).replace('am', 'AM').replace('pm', 'PM')
}

function formatSeconds(_seconds, includeSeconds = false) {
    const days = Math.floor(_seconds / (3600 * 24))
    _seconds = _seconds % (3600 * 24)
    const hours = _seconds / 3600
    _seconds = _seconds % 3600
    const minutes = _seconds / 60
    const seconds = _seconds % 60

    return `${days >= 1 ? days.toString() + (days > 1 ? ' days, ' : ' day, ') : ''}${Math.floor(hours).toString().padStart(2, '0')} : ${Math.floor(minutes).toString().padStart(2, '0')}${includeSeconds ? ' : ' + Math.floor(seconds).toString().padStart(2, '0') : ''}`
}


function compareDates(first, second) {
    const firstDate = new Date(first)
    const secondDate = new Date(second)
    return firstDate - secondDate
}

const platformIcons = {
    "AtCoder": AtCoder,
    "CodeChef": CodeChef,
    "Codeforces": Codeforces,
    "GeeksforGeeks": GeeksforGeeks,
    "LeetCode": LeetCode
}

export { formatDate, formatSeconds, compareDates, platformIcons }
