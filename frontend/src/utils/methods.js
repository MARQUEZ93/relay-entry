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
    // Convert the value to a floating point number
    value = parseFloat(value);
     // Check if the value is an integer (i.e., no decimal places)
    if (Number.isInteger(value)) {
      value = value.toString();  // Convert it back to a string without decimals
    } else {
      // Otherwise, format it to 2 decimal places, then strip any trailing .00
      value = value.toFixed(2);
      if (value.endsWith('.00')) {
          value = value.slice(0, -3);  // Remove the .00 part
      }
    }
  }

  return `${value}${race.custom_distance_unit}`;
}

export function formatMinute(minute) {
  return minute < 10 ? '0' + minute : minute;
}

  