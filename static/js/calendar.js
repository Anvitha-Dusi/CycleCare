/**
 * static/js/calendar.js
 * -----------------------------------------------------------------------------
 * Interactive Menstrual Cycle Calendar with Red Highlighted Period Days.
 * Demonstrates:
 * - Dynamic calendar generation using pure JavaScript date math
 * - Mapping date intervals (start_date to end_date) to calendar cells
 * - Highlighting logged period days in RED and estimated periods
 * - Responsive month navigation and interactive day inspection
 * -----------------------------------------------------------------------------
 */

let calendarCurrentDate = new Date();
let calendarAllCycles = [];
let calendarEstimatedPeriodStart = null;
let calendarAvgPeriodDuration = 5;

/**
 * Initializes or updates calendar with user cycle data.
 */
function initCalendar(cycles = [], estimatedStart = null, avgDuration = 5) {
  calendarAllCycles = cycles;
  calendarEstimatedPeriodStart = estimatedStart;
  calendarAvgPeriodDuration = avgDuration || 5;

  renderCalendar();
}

/**
 * Navigates to previous month.
 */
function prevMonth() {
  calendarCurrentDate.setMonth(calendarCurrentDate.getMonth() - 1);
  renderCalendar();
}

/**
 * Navigates to next month.
 */
function nextMonth() {
  calendarCurrentDate.setMonth(calendarCurrentDate.getMonth() + 1);
  renderCalendar();
}

/**
 * Resets calendar view to today's month.
 */
function goToTodayMonth() {
  calendarCurrentDate = new Date();
  renderCalendar();
}

/**
 * Helper to build YYYY-MM-DD string with local time safe format.
 */
function toDateKey(dateObj) {
  const y = dateObj.getFullYear();
  const m = String(dateObj.getMonth() + 1).padStart(2, '0');
  const d = String(dateObj.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

/**
 * Helper to parse a YYYY-MM-DD string into a local Date object.
 */
function parseLocalDate(dateStr) {
  if (!dateStr) return null;
  const parts = dateStr.split('-');
  return new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
}

/**
 * Builds a fast lookup map of dates that are recorded period days or estimated days.
 */
function buildPeriodDateMap() {
  const dateMap = {};

  // 1. Map recorded period days (HIGHLIGHTED IN RED)
  calendarAllCycles.forEach(cycle => {
    if (!cycle.start_date) return;
    const start = parseLocalDate(cycle.start_date);
    let end = parseLocalDate(cycle.end_date);

    if (!end) {
      end = new Date(start);
      end.setDate(end.getDate() + (cycle.period_duration || 5) - 1);
    }

    const current = new Date(start);
    let dayNum = 1;

    while (current <= end) {
      const key = toDateKey(current);
      dateMap[key] = {
        type: 'logged',
        dayOfPeriod: dayNum,
        totalDuration: cycle.period_duration,
        cycle: cycle
      };
      current.setDate(current.getDate() + 1);
      dayNum++;
    }
  });

  // 2. Map estimated upcoming period days
  if (calendarEstimatedPeriodStart) {
    const estStart = parseLocalDate(calendarEstimatedPeriodStart);
    if (estStart) {
      const estEnd = new Date(estStart);
      estEnd.setDate(estEnd.getDate() + calendarAvgPeriodDuration - 1);

      const current = new Date(estStart);
      while (current <= estEnd) {
        const key = toDateKey(current);
        // Only mark estimated if not already logged as real period
        if (!dateMap[key]) {
          dateMap[key] = {
            type: 'estimated',
            estStart: calendarEstimatedPeriodStart
          };
        }
        current.setDate(current.getDate() + 1);
      }
    }
  }

  return dateMap;
}

/**
 * Renders the calendar month grid and day cells.
 */
function renderCalendar() {
  const titleEl = document.getElementById('calendar-month-year');
  const gridEl = document.getElementById('calendar-grid-days');
  const detailEl = document.getElementById('calendar-day-detail');

  if (!titleEl || !gridEl) return;

  const year = calendarCurrentDate.getFullYear();
  const month = calendarCurrentDate.getMonth();

  // Set Month and Year Title
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  titleEl.textContent = `${monthNames[month]} ${year}`;

  const periodDateMap = buildPeriodDateMap();

  // First day of current month & total days
  const firstDayIndex = new Date(year, month, 1).getDay(); // 0 (Sun) to 6 (Sat)
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const prevMonthDays = new Date(year, month, 0).getDate();

  const todayStr = toDateKey(new Date());

  let daysHtml = '';

  // 1. Previous Month trailing days
  for (let x = firstDayIndex; x > 0; x--) {
    const day = prevMonthDays - x + 1;
    const prevDate = new Date(year, month - 1, day);
    const key = toDateKey(prevDate);
    const periodInfo = periodDateMap[key];

    let cellClass = 'calendar-day-cell other-month';
    let badgeHtml = '';

    if (periodInfo && periodInfo.type === 'logged') {
      cellClass += ' period-day';
      badgeHtml = `<span class="period-label">Period</span>`;
    } else if (periodInfo && periodInfo.type === 'estimated') {
      cellClass += ' estimated-day';
      badgeHtml = `<span class="estimated-label">Est</span>`;
    }

    daysHtml += `
      <div class="${cellClass}" onclick="selectCalendarDate('${key}')">
        <span class="day-number">${day}</span>
        ${badgeHtml}
      </div>
    `;
  }

  // 2. Current Month days
  for (let d = 1; d <= daysInMonth; d++) {
    const currentDate = new Date(year, month, d);
    const key = toDateKey(currentDate);
    const periodInfo = periodDateMap[key];

    let cellClass = 'calendar-day-cell';
    let badgeHtml = '';

    if (key === todayStr) {
      cellClass += ' is-today';
    }

    if (periodInfo) {
      if (periodInfo.type === 'logged') {
        // HIGHLIGHT IN RED
        cellClass += ' period-day';
        badgeHtml = `<span class="period-label">Period Day ${periodInfo.dayOfPeriod}</span>`;
      } else if (periodInfo.type === 'estimated') {
        cellClass += ' estimated-day';
        badgeHtml = `<span class="estimated-label">Estimated</span>`;
      }
    }

    daysHtml += `
      <div class="${cellClass}" onclick="selectCalendarDate('${key}')">
        <span class="day-number">${d}</span>
        ${badgeHtml}
      </div>
    `;
  }

  // 3. Next Month leading days to complete grid (total cells multiple of 7)
  const totalCellsSoFar = firstDayIndex + daysInMonth;
  const remainingCells = (totalCellsSoFar % 7 === 0) ? 0 : 7 - (totalCellsSoFar % 7);

  for (let y = 1; y <= remainingCells; y++) {
    const nextDate = new Date(year, month + 1, y);
    const key = toDateKey(nextDate);
    const periodInfo = periodDateMap[key];

    let cellClass = 'calendar-day-cell other-month';
    let badgeHtml = '';

    if (periodInfo && periodInfo.type === 'logged') {
      cellClass += ' period-day';
      badgeHtml = `<span class="period-label">Period</span>`;
    } else if (periodInfo && periodInfo.type === 'estimated') {
      cellClass += ' estimated-day';
      badgeHtml = `<span class="estimated-label">Est</span>`;
    }

    daysHtml += `
      <div class="${cellClass}" onclick="selectCalendarDate('${key}')">
        <span class="day-number">${y}</span>
        ${badgeHtml}
      </div>
    `;
  }

  gridEl.innerHTML = daysHtml;
}

/**
 * Handles selecting/clicking a specific date on the calendar.
 */
function selectCalendarDate(dateKey) {
  const detailEl = document.getElementById('calendar-day-detail');
  if (!detailEl) return;

  const dateObj = parseLocalDate(dateKey);
  const formatted = dateObj.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  const periodDateMap = buildPeriodDateMap();
  const info = periodDateMap[dateKey];

  if (info && info.type === 'logged') {
    const cycle = info.cycle;
    const notesStr = cycle.notes ? ` &bull; <em>"${escapeHtml(cycle.notes)}"</em>` : '';
    detailEl.innerHTML = `
      <div>
        <strong>📅 ${formatted}</strong>: 
        <span style="color: #dc2626; font-weight: 700;">🔴 Logged Period Day (Day ${info.dayOfPeriod} of ${cycle.period_duration} days)</span>
        ${notesStr}
      </div>
      <div>
        <button class="btn btn-outline btn-sm" onclick="openEditCycleModal(${cycle.id})">Edit Cycle</button>
      </div>
    `;
  } else if (info && info.type === 'estimated') {
    detailEl.innerHTML = `
      <div>
        <strong>📅 ${formatted}</strong>: 
        <span style="color: #be123c; font-weight: 700;">🌸 Estimated Upcoming Period Window</span>
        (Mathematical projection based on your historical cycle averages).
      </div>
      <div>
        <button class="btn btn-primary btn-sm" onclick="quickLogFromCalendar('${dateKey}')">+ Record Period Start</button>
      </div>
    `;
  } else {
    detailEl.innerHTML = `
      <div>
        <strong>📅 ${formatted}</strong>: Normal non-period day.
      </div>
      <div>
        <button class="btn btn-outline btn-sm" onclick="quickLogFromCalendar('${dateKey}')">+ Log Cycle Starting This Day</button>
      </div>
    `;
  }
}

/**
 * Quick action to pre-fill the Add Cycle modal with a clicked date.
 */
function quickLogFromCalendar(dateStr) {
  openAddCycleModal();
  const startInput = document.getElementById('cycle-start-date');
  if (startInput) {
    startInput.value = dateStr;
    updateEndDateFromDuration();
  }
}
