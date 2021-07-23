var cta = document.getElementById("mahasiswakuota").getContext("2d");
var myChart = new Chart(cta, {
  type: "bar",
  data: {
    labels: ["EISD", "EDE", "ERP", "SAG", "EIM"],
    datasets: [
      {
        label: "Mahasiswa",
        borderRadius: 2,
        data: [123, 67, 39, 95, 43],
        backgroundColor: "#2B73D7",
        fontColor: "white",
      },
      {
        label: "Kuota Peminatan",
        backgroundColor: "transparent",
        tension: 0,
        backgroundColor: "#FF6384",
        data: [120, 90, 50, 150, 60],
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: true,
      position: "top",
      labels: {
        fontColor: "#8898AA",
      },
    },
    scales: {
      yAxes: [
        {
          gridLines: {
            display: true,
          },
          ticks: {
            beginAtZero: true,
          },
        },
      ],
      xAxes: [
        {
          stacked: true,
          gridLines: {
            display: false,
          },
          ticks: {
            fontColor: "black",
          },
        },
      ],
    },

    tooltips: {
      enabled: true,
      mode: "index",
      intersect: true,
    },
  },
});

// kelompok keahlian
var ctb = document.getElementById("kelompokkeahlian").getContext("2d");
var ctc = document.getElementById("dosenpeminatan").getContext("2d");

var chart = new Chart(ctb, {
  type: "pie",
  data: {
    labels: ["Cybernetics", "EIS"],
    datasets: [
      {
        data: [21, 26],
        backgroundColor: ["#2B73D7", "#75A1DE"],
        labels: ["Cybernetics", "EIS"],
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    elements: {
      arc: {
        borderWidth: 0,
      },
    },
    title: {
      display: true,
      align: "end",
    },
    legend: {
      position: "right",
      labels: {
        boxWidth: 12,
      },
    },
  },
});

var cchart = new Chart(ctc, {
  type: "pie",
  data: {
    labels: ["EDE", "EISD", "EIM", "ERP", "SAG"],
    datasets: [
      {
        data: [9, 12, 6, 5, 15],
        backgroundColor: [
          "#f4f1de",
          "#e07a5f",
          "#3d405b",
          "#81b29a",
          "#f2cc8f",
        ],
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: true,
    elements: {
      arc: {
        borderWidth: 0,
      },
    },
    title: {
      display: true,
      align: "end",
    },
    legend: {
      position: "right",
      labels: {
        boxWidth: 12,
      },
    },
  },
});
