import type { Material } from "$lib/types";

export function convertKgToM(kgs: number, material: Material): number {
    const conversions = {
        "butter": (kgs * 3500) / 60,
        "uv_butter": (kgs * 3500) / 60,
        "lid": (kgs * 1500) / 28,
        "embossed_lid": (kgs * 1500) / 32,
    };
    return conversions[material];
}

export function calculateMinutesLength(quantityKgs: number, material: Material): number {
    const meters = convertKgToM(quantityKgs, material);
    const rollLength = {
        "lid": { "length": 1500, "roll_duration": 35 },
        "embossed_lid": { "length": 1500, "roll_duration": 35 },
        "butter": { "length": 3500, "roll_duration": 85 },
        "uv_butter": { "length": 3500, "roll_duration": 85 },
    };
    const runs = Math.ceil(meters / rollLength[material]["length"]);
    const breaks = runs - 1;
    return (breaks * 5) + (runs * rollLength[material]["roll_duration"]);
}
