$(function () {
  $("#content_wrapper").on("submit", "#crypto_form", function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      data: $(this).serialize(),
      dataType: "json",
      error: function (request, error) {
        console.log(arguments);
        console.log(" Can't do because: " + error);
      },
      success: function (data) {
        $("#msg_queue").html(data.msg_list);
        $("#wactchlist_wrapper").html(data.html);
      },
    });
  });
});

const sequential_ctx = document.getElementById('SequentialChart');
const hourly_ctx = document.getElementById('HourlyChart');

const sequential_data = {
  datasets: [{
    data: sequential_price,
    backgroundColor: '#ff6384',
    borderColor: '#ff6384',
    borderWidth: '1',
    label: 'Price',
    tension: 0.2,
    yAxisID: 'Price',
  }, {
    data: sequential_quant,
    backgroundColor: '#36a2eb',
    borderColor: '#36a2eb',
    borderWidth: '1',
    label: 'Quant',
    tension: 0.2,
    yAxisID: 'Quant',
  }],
  labels: sequential_labels
}


const hourly_data = {
  datasets: [{
    data: hourly_price,
    backgroundColor: '#ff6384',
    borderColor: '#ff6384',
    borderWidth: '1',
    label: 'Price',
    tension: 0.2,
    yAxisID: 'Price',
  }, {
    data: hourly_quant,
    backgroundColor: '#36a2eb',
    borderColor: '#36a2eb',
    borderWidth: '1',
    label: 'Quant',
    tension: 0.2,
    yAxisID: 'Quant',
  }],
  labels: hourly_labels
}

const options = {
  responsive: true,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  stacked: false,
  plugins: {
    title: {
      display: true,
      text: 'MinBuyout vs Quantity over 24 hours'
    }
  },
  scales: {
    Price: {
      beginAtZero: true,
      display: true,
      id: 'Price',
      type: 'linear',
      position: 'left',
      grid: {
        color: '#ff63852f',
        borderColor: '#ff63852f',
      },
      ticks: {
        color: "#ff6384"
      }
    },
    Quant: {
      beginAtZero: true,
      display: true,
      id: 'Quant',
      type: 'linear',
      position: 'right',
      grid: {
        color: '#36a3eb2f',
        borderColor: '#36a3eb2f'
      },
      ticks: {
        color: "#36a2eb"
      }
    }
  }
}
const SequentialChart = new Chart(sequential_ctx, {
  type: 'line',
  data: sequential_data,
  options: options
});

const HourlyChart = new Chart(sequential_ctx, {
  type: 'line',
  data: sequential_data,
  options: options
});