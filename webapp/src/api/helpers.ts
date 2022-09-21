export function contactNameFormat(name: string): string {
    let newName = `@${name}`;
    return newName
}

export function createdOnDateFormat(date: string): string {
    let dt = new Date(date);
    const month = dt.toLocaleString('default', { month: 'long' });
    let newDate = `Created on ${month} ${dt.getDate()}, ${dt.getFullYear()}`
    return newDate
}

export function phoneFormat(number: string): string {
    let areaCode = number.substring(2, 5);
    let p1 = number.substring(5, 8);
    let p2 = number.substring(8, 12);
    return `(${areaCode}) ${p1}-${p2}`
}
