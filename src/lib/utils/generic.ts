export const capitalizeString = (s: string) => {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

export const dbToAutocomplete = (items: {id: string | number, name:string}[])=>{
    return items.map((item) => {
		return { value: item.id, label: capitalizeString(item.name) };}
	)
}