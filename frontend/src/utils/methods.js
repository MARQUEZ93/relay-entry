/**
 * Formats a date to a UTC string.
 * @param {string} date - The date string.
 * @returns {string} - The formatted date string in UTC.
 */
export function formatDateToUTC(date) {
  const d = new Date(date);
  const year = d.getUTCFullYear();
  const month = d.toLocaleString('default', { month: 'long', timeZone: 'UTC' });
  const day = d.getUTCDate();
  return `${month} ${day}, ${year}`;
}
  
  /**
   * Formats a race date.
   * @param {string} date - The date string.
   * @returns {string|null} - The formatted race date or null if no date is provided.
   */
export function formattedRaceDate(date) {
  if (date) {
    return formatDateToUTC(date);
  }
  return null;
}

/**
 * Formats the custom distance value.
 * @param {Object} race - The race object containing custom distance values.
 * @returns {string} - The formatted custom distance value.
 */
export function customSameDistance(race) {
  if (!race.custom_distance_value || !race.custom_distance_unit) {
    return '';
  }

  let value = race.custom_distance_value;

  if (race.custom_distance_unit === 'm') {
    // Strip .00 decimal
    value = parseFloat(value).toFixed(2);
    if (value.endsWith('.00')) {
      value = value.slice(0, -3);
    }
  }

  return `${value}${race.custom_distance_unit}`;
}

export function formatMinute(minute) {
  return minute < 10 ? '0' + minute : minute;
}

  