/**
 * static/js/dashboard.js
 * -----------------------------------------------------------------------------
 * Dashboard data fetching, metric card rendering, and UI updates.
 * Demonstrates:
 * - Dynamic DOM rendering using vanilla JavaScript
 * - Consuming analytical REST API endpoints
 * - Conditional empty state handling
 * -----------------------------------------------------------------------------
 */

document.addEventListener('DOMContentLoaded', () => {
  loadDashboardData();
});

async function loadDashboardData() {
  const loadingIndicator = document.getElementById('dashboard-loading');
  const dashboardContent = document.getElementById('dashboard-content');

  try {
    const res = await fetch('/api/dashboard');
    if (res.status === 401) {
      window.location.href = '/login';
      return;
    }

    const data = await res.json();
    if (!res.ok || !data.success) {
      showToast(data.message || 'Failed to load dashboard data.', 'error');
      return;
    }

    renderDashboard(data);
  } catch (err) {
    console.error('Error loading dashboard:', err);
    showToast('Network error while loading dashboard.', 'error');
  }
}

function renderDashboard(data) {
  // Update Welcome message
  const welcomeEl = document.getElementById('dashboard-welcome');
  if (welcomeEl) {
    welcomeEl.textContent = data.welcome_message || 'Welcome to CycleCare!';
  }

  // Stat elements
  const totalCyclesEl = document.getElementById('stat-total-cycles');
  const avgCycleLengthEl = document.getElementById('stat-avg-cycle');
  const avgDurationEl = document.getElementById('stat-avg-duration');
  const lastPeriodEl = document.getElementById('stat-last-period');

  // Estimate banner elements
  const estimateBanner = document.getElementById('estimate-banner');
  const estimateDateEl = document.getElementById('estimate-date');
  const estimateFormulaEl = document.getElementById('estimate-formula');
  const estimateBadgeEl = document.getElementById('estimate-badge');

  // Recent cycles table
  const recentTableBody = document.getElementById('recent-cycles-body');
  const emptyStateEl = document.getElementById('cycles-empty-state');
  const tableContainer = document.getElementById('recent-cycles-table-container');

  if (totalCyclesEl) totalCyclesEl.textContent = data.total_cycles;

  if (data.has_data) {
    if (avgCycleLengthEl) avgCycleLengthEl.innerHTML = `${data.avg_cycle_length} <span class="stat-unit">days</span>`;
    if (avgDurationEl) avgDurationEl.innerHTML = `${data.avg_period_duration} <span class="stat-unit">days</span>`;
    
    if (lastPeriodEl && data.last_period) {
      lastPeriodEl.textContent = formatDate(data.last_period.start_date);
    }

    // Populate Estimate Banner
    if (estimateBanner) estimateBanner.style.display = 'flex';
    if (estimateDateEl) estimateDateEl.textContent = data.estimated_next_period_formatted;
    if (estimateFormulaEl) estimateFormulaEl.textContent = data.formula_explanation;

    if (estimateBadgeEl) {
      const days = data.days_until_next;
      if (days > 1) {
        estimateBadgeEl.textContent = `In ~${days} days`;
      } else if (days === 1) {
        estimateBadgeEl.textContent = 'Tomorrow';
      } else if (days === 0) {
        estimateBadgeEl.textContent = 'Expected Today';
      } else {
        estimateBadgeEl.textContent = `${Math.abs(days)} days ago`;
      }
    }

    // Populate recent cycles
    if (recentTableBody && data.recent_cycles.length > 0) {
      if (emptyStateEl) emptyStateEl.style.display = 'none';
      if (tableContainer) tableContainer.style.display = 'block';

      recentTableBody.innerHTML = data.recent_cycles.map(cycle => `
        <tr>
          <td><strong>${formatDate(cycle.start_date)}</strong></td>
          <td>${cycle.end_date ? formatDate(cycle.end_date) : '—'}</td>
          <td><span class="badge-tag badge-primary">${cycle.period_duration} days</span></td>
          <td><span class="badge-tag badge-neutral">${cycle.cycle_length} days</span></td>
          <td style="max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            ${cycle.notes ? escapeHtml(cycle.notes) : '<span style="color: var(--color-text-light);">None</span>'}
          </td>
          <td>
            <div class="table-actions">
              <button class="btn btn-outline btn-sm" onclick="openEditCycleModal(${cycle.id})">Edit</button>
              <button class="btn btn-danger btn-sm" onclick="openDeleteModal(${cycle.id})">Delete</button>
            </div>
          </td>
        </tr>
      `).join('');
    }
  } else {
    // Zero data state
    if (avgCycleLengthEl) avgCycleLengthEl.textContent = '—';
    if (avgDurationEl) avgDurationEl.textContent = '—';
    if (lastPeriodEl) lastPeriodEl.textContent = 'None yet';

    if (estimateBanner) estimateBanner.style.display = 'none';
    if (tableContainer) tableContainer.style.display = 'none';
    if (emptyStateEl) emptyStateEl.style.display = 'block';
  }

  // Initialize and render the Cycle Calendar with red highlights
  if (typeof initCalendar === 'function') {
    const cyclesList = data.all_cycles || data.recent_cycles || [];
    initCalendar(cyclesList, data.estimated_next_period, data.avg_period_duration);
  }
}

/**
 * Format date string YYYY-MM-DD into readable format (e.g., Oct 01, 2026).
 */
function formatDate(dateStr) {
  if (!dateStr) return '—';
  try {
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      const year = parseInt(parts[0], 10);
      const month = parseInt(parts[1], 10) - 1;
      const day = parseInt(parts[2], 10);
      const d = new Date(year, month, day);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
    return dateStr;
  } catch (e) {
    return dateStr;
  }
}

/**
 * Basic HTML escaping helper to prevent XSS.
 */
function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
