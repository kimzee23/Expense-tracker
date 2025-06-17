document.addEventListener("DOMContentLoaded", () => {
  const userId = localStorage.getItem("user_id");

  if (!userId) {
    console.warn("No user_id found. Redirecting...");
    window.location.href = "/login";
    return;
  }

  const dashboardReady = document.getElementById("dashboardContainer");
  const budgetForm = document.getElementById("budgetForm");
  const budgetInput = document.getElementById("budgetInput");

  const budgetAmountEl = document.getElementById("budgetAmount");
  const expensesTotalEl = document.getElementById("expensesTotal");
  const remainingBudgetEl = document.getElementById("remainingBudget");
  const recentExpensesList = document.getElementById("recentExpensesList");

  const lineCtx = document.getElementById("lineChart")?.getContext("2d");
  const categoryCtx = document.getElementById("categoryChart")?.getContext("2d");
  const timeCtx = document.getElementById("timeChart")?.getContext("2d");

  let lineChart, categoryChart, timeChart;

  async function fetchDashboardData() {
    try {
      const [budgetRes, reportRes] = await Promise.all([
        fetch(`/api/v1/budgets/${userId}`),
        fetch(`/api/v1/reports/?user_id=${userId}`)
      ]);

      const budget = await budgetRes.json();
      const report = await reportRes.json();

      const total = budget.amount || 0;
      const spent = report.total_expense || 0;
      const remain = total - spent;

      if (budgetAmountEl) budgetAmountEl.textContent = `Total Budget: ₦${total}`;
      if (expensesTotalEl) expensesTotalEl.textContent = `Total Spent: ₦${spent}`;
      if (remainingBudgetEl) remainingBudgetEl.textContent = `Remaining: ₦${remain}`;

      if (recentExpensesList) {
        recentExpensesList.innerHTML = (report.recent_expenses || [])
          .map(e => `<div class="expense-item"><strong>${e.title}</strong> - ₦${e.amount} <em>(${e.category})</em></div>`)
          .join("");
      }

      if (lineCtx && report.expenses_by_date) {
        if (lineChart) lineChart.destroy();
        lineChart = new Chart(lineCtx, {
          type: "line",
          data: {
            labels: report.expenses_by_date.map(e => e.date),
            datasets: [{
              label: "Expenses Over Time",
              data: report.expenses_by_date.map(e => e.total),
              borderColor: "#d4ff00",
              backgroundColor: "rgba(212, 255, 0, 0.2)",
              tension: 0.4,
              fill: true
            }]
          }
        });
      }

      if (categoryCtx && report.expenses_by_category) {
        const categories = Object.keys(report.expenses_by_category);
        const categoryData = Object.values(report.expenses_by_category);
        if (categoryChart) categoryChart.destroy();
        categoryChart = new Chart(categoryCtx, {
          type: "doughnut",
          data: {
            labels: categories,
            datasets: [{
              label: "Spending by Category",
              data: categoryData,
              backgroundColor: ["#d4ff00", "#4caf50", "#ff9800", "#00bcd4", "#e91e63", "#9c27b0"]
            }]
          }
        });
      }

      if (timeCtx && report.expenses_by_hour) {
        const hourLabels = report.expenses_by_hour.map(e => `${e.hour}:00`);
        const hourValues = report.expenses_by_hour.map(e => e.total);
        if (timeChart) timeChart.destroy();
        timeChart = new Chart(timeCtx, {
          type: "bar",
          data: {
            labels: hourLabels,
            datasets: [{
              label: "Spending by Time of Day",
              data: hourValues,
              backgroundColor: "#d4ff00"
            }]
          }
        });
      }
    } catch (err) {
      console.error("Dashboard data fetch error:", err);
    }
  }

  // === Submit Budget Form ===
  if (budgetForm) {
    budgetForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const amount = parseFloat(budgetInput.value);
      if (isNaN(amount)) {
        alert("Enter a valid budget amount.");
        return;
      }

      const today = new Date();
      const nextMonth = new Date();
      nextMonth.setMonth(today.getMonth() + 1);

      const payload = {
        user_id: userId,
        amount: amount,
        start_date: today.toISOString(),
        end_date: nextMonth.toISOString()
      };

      try {
        const res = await fetch("/api/v1/budgets", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          alert("Budget saved!");
          await fetchDashboardData();
        } else {
          const error = await res.json();
          alert("Failed to save budget: " + (error.error || "Unknown error"));
        }
      } catch (err) {
        console.error("Error saving budget:", err);
        alert("Error saving budget.");
      }
    });
  }
const expenseForm = document.getElementById("addExpenseForm");

if (expenseForm) {
  expenseForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(expenseForm);
    const title = formData.get("title");
    const amount = parseFloat(formData.get("amount"));
    const category = formData.get("category");
    const description = formData.get("description");
    const userId = localStorage.getItem("user_id");

    if (!userId) {
      alert("User not logged in.");
      return;
    }

    if (!title || isNaN(amount) || !category) {
      alert("Please fill out all fields correctly.");
      return;
    }

    const payload = {
      title,
      amount,
      category,
      description,
      user_id: userId,
      date: new Date().toISOString()
    };

    try {
      const res = await fetch("/api/v1/expenses/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        alert("Expense added successfully!");
        expenseForm.reset();
        fetchDashboardData();
      } else {
        const error = await res.json();
        alert("Failed to add expense: " + (error.error || "Unknown error"));
      }
    } catch (err) {
      console.error("Add expense error:", err);
      alert("Something went wrong.");
    }
  });
}


  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.onclick = () => {
      localStorage.removeItem("user_id");
      window.location.href = "/login";
    };
  }

  if (dashboardReady) {
    fetchDashboardData();
  }
});
