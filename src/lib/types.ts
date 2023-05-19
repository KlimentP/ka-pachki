export type Material = "butter" | "lid" | "embossed_lid" | "uv_butter";
export type Machine = "butter" | "label" | "embossed_lid";

export const Machines: { [K in Machine]: string } = {
    butter: "Butter",
    label: "Labels",
    embossed_lid: "Embossed Lids"
  }