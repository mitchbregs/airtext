export function phoneFormat(number: string): string {
    let countryCode = number.substring(0, 2)
    let areaCode = number.substring(2, 5)
    let start = number.substring(5, 8)
    let end = number.substring(8, 12)
    return `${countryCode} (${areaCode}) ${start}-${end}`
}
