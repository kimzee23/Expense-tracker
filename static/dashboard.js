document.addEventListener("DOMContentLoaded", () => {
  const userId = localStorage.getItem("user_id");
  console.log("Current logged in user:", userId);

  if (!userId && window.location.pathname.includes("dashboard")) {
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
  const expenseForm = document.getElementById("addExpenseForm");
  const logoutBtn = document.getElementById("logoutBtn");
  const registerForm = document.getElementById("registerForm");

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

      const total = budget?.amount ?? 0;
      const spent = report.total_expense || 0;
      const remain = total - spent;

      budgetAmountEl.textContent = `Total Budget: ₦${total}`;
      expensesTotalEl.textContent = `Total Spent: ₦${spent}`;
      remainingBudgetEl.textContent = `Remaining: ₦${remain}`;

      recentExpensesList.innerHTML = (report.recent_expenses || [])
        .map(e => `
          <div class="expense-item">
            <strong>${e.title}</strong> - ₦${e.amount} <em>(${e.category})</em>
            <button class="delete-expense" data-id="${e.id}">Delete</button>
          </div>
        `)
        .join("");

      if (lineCtx && report.expenses_by_date?.length) {
        lineChart?.destroy();
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

      if (categoryCtx && report.expenses_by_category && Object.keys(report.expenses_by_category).length > 0) {
        categoryChart?.destroy();
        categoryChart = new Chart(categoryCtx, {
          type: "doughnut",
          data: {
            labels: Object.keys(report.expenses_by_category),
            datasets: [{
              label: "Spending by Category",
              data: Object.values(report.expenses_by_category),
              backgroundColor: ["#d4ff00", "#4caf50", "#ff9800", "#00bcd4", "#e91e63", "#9c27b0"]
            }]
          }
        });
      }

      if (timeCtx && report.expenses_by_hour?.length) {
        timeChart?.destroy();
        timeChart = new Chart(timeCtx, {
          type: "bar",
          data: {
            labels: report.expenses_by_hour.map(e => `${e.hour}:00`),
            datasets: [{
              label: "Spending by Time of Day",
              data: report.expenses_by_hour.map(e => e.total),
              backgroundColor: "#d4ff00"
            }]
          }
        });
      }

    } catch (err) {
      console.error("Dashboard data fetch error:", err);
    }
  }

  if (budgetForm) {
    budgetForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const amount = parseFloat(budgetInput.value.trim());
      if (isNaN(amount) || amount <= 0) {
        alert("Please enter a valid budget amount.");
        return;
      }

      const today = new Date();
      const nextMonth = new Date();
      nextMonth.setMonth(today.getMonth() + 1);

      const payload = {
        user_id: userId,
        amount,
        start_date: today.toISOString(),
        end_date: nextMonth.toISOString()
      };

      try {
        const res = await fetch("/api/v1/budgets/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const result = await res.json();
        if (res.ok) {
          alert("Budget saved!");
          await fetchDashboardData();
        } else {
          alert("Failed to save budget: " + (result.error || "Unknown error"));
        }
      } catch (err) {
        console.error("Error saving budget:", err);
        alert("Error saving budget.");
      }
    });
  }

  if (expenseForm) {
    expenseForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(expenseForm);
      const title = formData.get("title")?.trim();
      const amount = parseFloat(formData.get("amount"));
      const category = formData.get("category");
      const description = formData.get("description")?.trim();

      if (!title || isNaN(amount) || amount <= 0 || !category || !description) {
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

        const result = await res.json();
        if (res.ok) {
          alert("Expense added successfully!");
          expenseForm.reset();
          fetchDashboardData();
        } else {
          alert("Failed to add expense: " + (result.error || "Unknown error"));
        }
      } catch (err) {
        console.error("Add expense error:", err);
        alert("Something went wrong.");
      }
    });
  }

  const deleteBudgetBtn = document.getElementById("deleteBudgetBtn");

  if (deleteBudgetBtn) {
    deleteBudgetBtn.addEventListener("click", async () => {
      if (!confirm("Are you sure you want to delete your budget?")) return;

      try {
        const res = await fetch(`/api/v1/budgets/${userId}`, {
          method: "DELETE"
        });

        const result = await res.json();
        if (res.ok) {
          alert("Budget deleted.");
          await fetchDashboardData();
        } else {
          alert("Failed to delete: " + (result.error || "Unknown error"));
        }
      } catch (err) {
        console.error("Delete budget error:", err);
        alert("Something went wrong.");
      }
    });
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("user_id");
      window.location.href = "/login";
    });
  }

  if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
      const password = document.getElementById("password")?.value?.trim();
      const phone = document.getElementById("phone")?.value?.trim();

      if (!password || password.length < 8) {
        alert("Password must be at least 8 characters long.");
        e.preventDefault();
        return;
      }

      const phoneRegex = /^\+234\d{10}$/;
      if (!phoneRegex.test(phone)) {
        alert("Phone number must start with +234 and contain exactly 13 digits.");
        e.preventDefault();
        return;
      }
    });
  }

  if (dashboardReady) {
    fetchDashboardData().catch(console.error);
  }
});
