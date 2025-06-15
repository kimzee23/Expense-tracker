document.addEventListener("DOMContentLoaded", async () => {
  const userId = localStorage.getItem("user_id");
  if (!userId) {
    window.location.href = "/login";
    return;
  }

  const budgetAmount = document.getElementById("budgetAmount");
  const expensesTotal = document.getElementById("expensesTotal");
  const remainingBudget = document.getElementById("remainingBudget");
  const recentExpensesDiv = document.getElementById("recentExpenses");

  const lineCtx = document.getElementById("lineChart").getContext("2d");
  const doughnutCtx = document.getElementById("doughnutChart").getContext("2d");

  // Initialize charts
  let lineChart, doughnutChart;

  const fetchDashboardData = async () => {
    try {
      // Get budget
      const budgetRes = await fetch(`/api/v1/budgets/${userId}`);
      const budgetData = await budgetRes.json();
      budgetAmount.textContent = `₦${budgetData.amount || 0}`;

      // Get report (summary)
      const reportRes = await fetch(`/api/v1/reports/?user_id=${userId}`);
      const reportData = await reportRes.json();

      expensesTotal.textContent = `₦${reportData.total_expense || 0}`;
      remainingBudget.textContent = `₦${(budgetData.amount || 0) - (reportData.total_expense || 0)}`;

      // Update recent expenses
      recentExpensesDiv.innerHTML = reportData.recent_expenses.map(exp => `
        <div class="expense-item">
          <strong>${exp.title}</strong> - ₦${exp.amount} <em>(${exp.category})</em>
        </div>
      `).join("");

      // Line Chart: expenses over time
      const lineLabels = reportData.expenses_by_date.map(d => d.date);
      const lineData = reportData.expenses_by_date.map(d => d.total);

      if (lineChart) lineChart.destroy();
      lineChart = new Chart(lineCtx, {
        type: "line",
        data: {
          labels: lineLabels,
          datasets: [{
            label: "Expenses Over Time",
            data: lineData,
            borderColor: "#9acd32",
            backgroundColor: "rgba(154,205,50,0.2)",
            fill: true,
            tension: 0.3
          }]
        }
      });

      // Doughnut Chart: expenses by category
      const categories = Object.keys(reportData.expenses_by_category || {});
      const categoryTotals = Object.values(reportData.expenses_by_category || {});

      if (doughnutChart) doughnutChart.destroy();
      doughnutChart = new Chart(doughnutCtx, {
        type: "doughnut",
        data: {
          labels: categories,
          datasets: [{
            label: "By Category",
            data: categoryTotals,
            backgroundColor: [
              "#9acd32", "#556b2f", "#8fbc8f", "#6b8e23", "#2e8b57", "#90ee90"
            ]
          }]
        }
      });

    } catch (error) {
      console.error("Error loading dashboard:", error);
    }
  };

  // Submit new expense
  const addExpenseForm = document.getElementById("addExpenseForm");
  addExpenseForm.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(addExpenseForm);
    const payload = {
      title: formData.get("title"),
      amount: Number(formData.get("amount")),
      category: formData.get("category"),
      user_id: userId
    };

    const res = await fetch("/api/v1/expenses/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      addExpenseForm.reset();
      await fetchDashboardData(); // refresh UI
    } else {
      const data = await res.json();
      alert("Error: " + (data.error || "Unable to add expense."));
    }
  };

  // Initial load
  fetchDashboardData();
});
