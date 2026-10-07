/**
 * static/js/cycles.js
 * -----------------------------------------------------------------------------
 * Cycle CRUD operations and modal controllers for CycleCare.
 * Demonstrates:
 * - Dynamic modal lifecycle and form auto-population
 * - REST API operations: POST, PUT, DELETE with fetch()
 * - Date math and synchronized duration calculation
 * - User confirmation workflows for record deletion
 * -----------------------------------------------------------------------------
 */

// Global delete target tracker
let cycleIdToDelete = null;

// Modal elements
const cycleModal = document.getElementById('cycle-modal');
const cycleModalTitle = document.getElementById('cycle-modal-title');
const cycleForm = document.getElementById('cycle-form');
const cycleIdInput = document.getElementById('cycle-id');
const startDateInput = document.getElementById('cycle-start-date');
const endDateInput = document.getElementById('cycle-end-date');
const durationInput = document.getElementById('cycle-duration');
const lengthInput = document.getElementById('cycle-length');
const notesInput = document.getElementById('cycle-notes');

const deleteModal = document.getElementById('delete-modal');

/**
 * Opens the Cycle Modal in Add Mode.
 */
function openAddCycleModal() {
  if (!cycleModal) return;
  cycleForm.reset();
  cycleIdInput.value = '';
  cycleModalTitle.textContent = 'Record Menstrual Cycle';
  
  // Set default start date to today
  const today = new Date().toISOString().split('T')[0];
  startDateInput.value = today;
  durationInput.value = 5;
  lengthInput.value = 28;
  updateEndDateFromDuration();

  cycleModal.classList.add('active');
}

/**
 * Opens the Cycle Modal in Edit Mode with existing record data.
 */
async function openEditCycleModal(cycleId) {
  if (!cycleModal) return;
  try {
    const res = await fetch(`/api/cycles/${cycleId}`);
    const data = await res.json();

    if (res.ok && data.success) {
      const cycle = data.cycle;
      cycleIdInput.value = cycle.id;
      startDateInput.value = cycle.start_date || '';
      endDateInput.value = cycle.end_date || '';
      durationInput.value = cycle.period_duration || 5;
      lengthInput.value = cycle.cycle_length || 28;
      notesInput.value = cycle.notes || '';

      cycleModalTitle.textContent = 'Edit Cycle Record';
      cycleModal.classList.add('active');
    } else {
      showToast(data.message || 'Unable to load cycle details.', 'error');
    }
  } catch (err) {
    console.error('Error fetching cycle for edit:', err);
    showToast('Failed to load cycle record.', 'error');
  }
}

/**
 * Closes the Cycle Modal.
 */
function closeCycleModal() {
  if (cycleModal) {
    cycleModal.classList.remove('active');
  }
}

/**
 * Opens delete confirmation modal.
 */
function openDeleteModal(cycleId) {
  cycleIdToDelete = cycleId;
  if (deleteModal) {
    deleteModal.classList.add('active');
  }
}

/**
 * Closes delete confirmation modal.
 */
function closeDeleteModal() {
  cycleIdToDelete = null;
  if (deleteModal) {
    deleteModal.classList.remove('active');
  }
}

/**
 * Helper to automatically synchronize end date based on start date and duration.
 */
function updateEndDateFromDuration() {
  if (!startDateInput.value || !durationInput.value) return;
  const days = parseInt(durationInput.value, 10);
  if (isNaN(days) || days < 1) return;

  const start = new Date(startDateInput.value + 'T00:00:00');
  start.setDate(start.getDate() + (days - 1));
  endDateInput.value = start.toISOString().split('T')[0];
}

/**
 * Helper to synchronize duration if user manually selects an end date.
 */
function updateDurationFromEndDate() {
  if (!startDateInput.value || !endDateInput.value) return;
  const start = new Date(startDateInput.value + 'T00:00:00');
  const end = new Date(endDateInput.value + 'T00:00:00');
  
  if (end >= start) {
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    durationInput.value = diffDays;
  }
}

// Attach date synchronization listeners
if (startDateInput && durationInput && endDateInput) {
  durationInput.addEventListener('input', updateEndDateFromDuration);
  startDateInput.addEventListener('change', updateEndDateFromDuration);
  endDateInput.addEventListener('change', updateDurationFromEndDate);
}

// -----------------------------------------------------------------------------
// Cycle Form Submission (Create or Update)
// -----------------------------------------------------------------------------
if (cycleForm) {
  cycleForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const cycleId = cycleIdInput.value;
    const isEdit = Boolean(cycleId);

    const payload = {
      start_date: startDateInput.value,
      end_date: endDateInput.value || null,
      period_duration: parseInt(durationInput.value, 10),
      cycle_length: parseInt(lengthInput.value, 10),
      notes: notesInput.value.trim()
    };

    // Client-side validation
    if (!payload.start_date) {
      showToast('Please select a start date.', 'error');
      return;
    }

    if (isNaN(payload.period_duration) || payload.period_duration < 1 || payload.period_duration > 30) {
      showToast('Period duration must be between 1 and 30 days.', 'error');
      return;
    }

    if (isNaN(payload.cycle_length) || payload.cycle_length < 15 || payload.cycle_length > 90) {
      showToast('Cycle length must be between 15 and 90 days.', 'error');
      return;
    }

    const saveBtn = document.getElementById('btn-save-cycle');
    if (saveBtn) {
      saveBtn.disabled = true;
      saveBtn.textContent = isEdit ? 'Updating...' : 'Saving...';
    }

    try {
      const url = isEdit ? `/api/cycles/${cycleId}` : '/api/cycles';
      const method = isEdit ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showToast(result.message || 'Cycle recorded successfully!', 'success');
        closeCycleModal();
        
        // Refresh page-specific view data
        if (typeof loadDashboardData === 'function') {
          loadDashboardData();
        } else if (typeof loadHistoryData === 'function') {
          loadHistoryData();
        } else {
          window.location.reload();
        }
      } else {
        showToast(result.message || 'Failed to save cycle record.', 'error');
      }
    } catch (err) {
      console.error('Error saving cycle:', err);
      showToast('Network error while saving cycle record.', 'error');
    } finally {
      if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Save Record';
      }
    }
  });
}

// -----------------------------------------------------------------------------
// Confirm Record Deletion Handler
// -----------------------------------------------------------------------------
const confirmDeleteBtn = document.getElementById('btn-confirm-delete');
if (confirmDeleteBtn) {
  confirmDeleteBtn.addEventListener('click', async () => {
    if (!cycleIdToDelete) return;

    confirmDeleteBtn.disabled = true;
    confirmDeleteBtn.textContent = 'Deleting...';

    try {
      const response = await fetch(`/api/cycles/${cycleIdToDelete}`, {
        method: 'DELETE'
      });
      const result = await response.json();

      if (response.ok && result.success) {
        showToast(result.message || 'Record deleted successfully.', 'success');
        closeDeleteModal();

        // Refresh views
        if (typeof loadDashboardData === 'function') {
          loadDashboardData();
        } else if (typeof loadHistoryData === 'function') {
          loadHistoryData();
        } else {
          window.location.reload();
        }
      } else {
        showToast(result.message || 'Failed to delete record.', 'error');
      }
    } catch (err) {
      console.error('Error deleting record:', err);
      showToast('Network error while deleting record.', 'error');
    } finally {
      confirmDeleteBtn.disabled = false;
      confirmDeleteBtn.textContent = 'Yes, Delete Record';
    }
  });
}

// -----------------------------------------------------------------------------
// User Logout Handler
// -----------------------------------------------------------------------------
async function handleLogout() {
  try {
    const res = await fetch('/api/logout', { method: 'POST' });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast('Logged out successfully.', 'success');
      setTimeout(() => {
        window.location.href = '/login';
      }, 500);
    }
  } catch (err) {
    console.error('Logout error:', err);
    window.location.href = '/login';
  }
}
