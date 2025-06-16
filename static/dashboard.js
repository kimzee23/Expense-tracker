document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  const userId = localStorage.getItem("user_id");

  window.onload = () => {
  fetchDashboardData();

  document.getElementById("budgetForm").onsubmit = async (e) => {
    e.preventDefault();

    const budgetAmount = parseFloat(document.getElementById("budgetInput").value);
    if (isNaN(budgetAmount)) {
      alert("Please enter a valid budget amount.");
      return;
    }

    const today = new Date();
    const oneMonthLater = new Date();
    oneMonthLater.setMonth(today.getMonth() + 1);

    const payload = {
      user_id: userId,
      amount: budgetAmount,
      start_date: today.toISOString(),
      end_date: oneMonthLater.toISOString()
    };

    try {
      const res = await fetch("/api/v1/budgets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        alert("Budget saved successfully.");
        fetchDashboardData(); // Update dashboard
      } else {
        const errorData = await res.json();
        alert("Failed to save budget: " + errorData.error);
      }
    } catch (err) {
      console.error("Error saving budget:", err);
      alert("Error saving budget.");
    }
  };
};


  // === LOGIN LOGIC ===
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.onsubmit = async (e) => {
      e.preventDefault();
      const payload = {
        email: loginForm.email.value,
        password: loginForm.password.value
      };

      const res = await fetch("/api/v1/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("user_id", data.user_id);
        window.location.href = "/dashboard";
      } else {
        const err = await res.json();
        alert("Login failed: " + (err.error || "Invalid credentials"));
      }
    };
    return; // only run login logic on login page
  }

  // === MY DASHBOARD LOGIC ===
  const dashboardReady = document.getElementById("dashboardContainer");
  if (dashboardReady) {
    if (!userId) {
      window.location.href = "/login";
      return;
    }

    const budgetAmount = document.getElementById("budgetAmount");
    const expensesTotal = document.getElementById("expensesTotal");
    const remainingBudget = document.getElementById("remainingBudget");
    const recentExpensesList = document.getElementById("recentExpensesList");

    const lineCtx = document.getElementById("lineChart")?.getContext("2d");
    const categoryCtx = document.getElementById("categoryChart")?.getContext("2d");
    const timeCtx = document.getElementById("timeChart")?.getContext("2d");

    let lineChart, categoryChart, timeChart;

    async function fetchDashboardData() {
      try {
        const budgetRes = await fetch(`/api/v1/budgets/${userId}`);
        const budgetData = await budgetRes.json();
        const reportRes = await fetch(`/api/v1/reports/?user_id=${userId}`);
        const reportData = await reportRes.json();

        const budget = budgetData.amount || 0;
        const spent = reportData.total_expense || 0;
        const remaining = budget - spent;

        budgetAmount.textContent = `Total Budget: ₦${budget}`;
        expensesTotal.textContent = `Total Spent: ₦${spent}`;
        remainingBudget.textContent = `Remaining: ₦${remaining}`;

        recentExpensesList.innerHTML = reportData.recent_expenses.map(exp => `
          <div class="expense-item">
            <strong>${exp.title}</strong> - ₦${exp.amount} <em>(${exp.category})</em>
          </div>
        `).join("");

        // Line Chart
        const dates = reportData.expenses_by_date.map(e => e.date);
        const amounts = reportData.expenses_by_date.map(e => e.total);
        if (lineCtx) {
          if (lineChart) lineChart.destroy();
          lineChart = new Chart(lineCtx, {
            type: "line",
            data: {
              labels: dates,
              datasets: [{
                label: "Expenses Over Time",
                data: amounts,
                borderColor: "#d4ff00",
                backgroundColor: "rgba(212, 255, 0, 0.2)",
                tension: 0.4,
                fill: true
              }]
            }
          });
        }

        // Doughnut Chart
        const categories = Object.keys(reportData.expenses_by_category || {});
        const categoryData = Object.values(reportData.expenses_by_category || {});
        if (categoryCtx) {
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

        // Bar Chart
        const hourLabels = reportData.expenses_by_hour?.map(e => `${e.hour}:00`) || [];
        const hourValues = reportData.expenses_by_hour?.map(e => e.total) || [];
        if (timeCtx) {
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
        console.error("Dashboard fetch error:", err);
      }
    }

    // Add Expense
    const addForm = document.getElementById("addExpenseForm");
    if (addForm) {
      addForm.onsubmit = async (e) => {
        e.preventDefault();
        const form = e.target;
        const payload = {
          title: form.title.value,
          amount: parseFloat(form.amount.value),
          category: form.category.value,
          date: new Date().toISOString(),
          description: form.title.value,
          user_id: userId
        };

        const res = await fetch("/api/v1/expenses/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          form.reset();
          fetchDashboardData();
        } else {
          const data = await res.json();
          alert("Failed to add expense: " + (data.error || "Unknown error"));
        }
      };
    }

    // Logout
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
      logoutBtn.onclick = () => {
        localStorage.removeItem("user_id");
        window.location.href = "/login";
      };
    }

    fetchDashboardData();
  }
});
