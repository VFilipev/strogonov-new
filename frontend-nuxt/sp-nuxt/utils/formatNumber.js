export function formatNumber(num) {
  if (num === null || num === undefined) return "0";
  return Number(num).toLocaleString("ru-RU", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
}
