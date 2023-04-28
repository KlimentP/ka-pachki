export const capitalizeString = (s: string) => {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

export const dbToAutocomplete = (items: {id: string | number, name:string}[])=>{
    return items.map((item) => {
		return { value: item.id, label: capitalizeString(item.name) };}
	)
}

export const  removeNullValues = (obj: {[key: string]: any | null | undefined}) => {
    return Object.entries(obj)
      .filter(([_, value]) => value !== null && value !== undefined)
      .reduce((newObj: {[key: string]: any}, [key, value]) => {
        newObj[key] = value;
        return newObj;
      }, {});
  }