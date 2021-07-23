var myChart, chart;
var cta = document.getElementById("mahasiswakuota").getContext("2d");
var ctx = document.getElementById("pemenuhan");

fetch("/api/bi/datapeminatan")
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    myChart = new Chart(cta, {
      type: "bar",
      data: {
        labels: ["EISD"],
        datasets: [
          {
            label: "Mahasiswa",
            borderRadius: 2,
            data: [data["eisd"]["mahasiswa"]],
            backgroundColor: "#2B73D7",
            fontColor: "white",
          },
          {
            label: "Kuota",
            tension: 0,
            backgroundColor: "#FF6384",
            data: [data["eisd"]["kuota"]],
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        legend: {
          display: true,
          position: "bottom",
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
                max:
                  data["eisd"]["kuota"] > data["eisd"]["mahasiswa"]
                    ? data["eisd"]["kuota"]
                    : data["eisd"]["mahasiswa"],
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

    chart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Terisi", "Kosong"],
        datasets: [
          {
            label: "Gauge",
            data: [
              (
                (data["eisd"]["mahasiswa"] / data["eisd"]["kuota"]) *
                100
              ).toFixed(1) > 100
                ? 100
                : (
                    (data["eisd"]["mahasiswa"] / data["eisd"]["kuota"]) *
                    100
                  ).toFixed(1),
              (
                (data["eisd"]["mahasiswa"] / data["eisd"]["kuota"]) *
                100
              ).toFixed(1) > 100
                ? 0
                : 100 -
                  (
                    (data["eisd"]["mahasiswa"] / data["eisd"]["kuota"]) *
                    100
                  ).toFixed(1),
            ],
            backgroundColor: ["rgb(54, 162, 235)", "rgb(255, 99, 132)"],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          datalabels: {
            backgroundColor: "rgba(0, 0, 0, 0.7)",
            borderColor: "#ffffff",
            color: function (context) {
              return context.dataset.backgroundColor;
            },
            font: function (context) {
              var w = context.chart.width;
              return {
                size: w < 512 ? 18 : 20,
              };
            },
          },
        },
        legend: {
          display: false,
        },
        tooltips: {
          enabled: true,
        },
      },
    });

    document.getElementById("pemenuhan-number").innerHTML = `${(
      (data["eisd"]["mahasiswa"] / data["eisd"]["kuota"]) *
      100
    ).toFixed(1)} %`;
    document.getElementById("ratio").innerHTML = `${parseInt(
      data["eisd"]["bimbingan"]
    )}`;

    document.getElementById("peminatan").addEventListener("change", (event) => {
      myChart.data.datasets[0].data = [
        data[event.target.value.toLowerCase()]["mahasiswa"],
      ];
      myChart.data.datasets[1].data = [
        data[event.target.value.toLowerCase()]["kuota"],
      ];
      myChart.options.scales.yAxes[0].ticks.max =
        data[event.target.value.toLowerCase()]["kuota"];

      chart.data.datasets[0].data = [
        (
          (data[event.target.value.toLowerCase()]["mahasiswa"] /
            data[event.target.value.toLowerCase()]["kuota"]) *
          100
        ).toFixed(1) > 100
          ? 100
          : (
              (data[event.target.value.toLowerCase()]["mahasiswa"] /
                data[event.target.value.toLowerCase()]["kuota"]) *
              100
            ).toFixed(1),
        (
          (data[event.target.value.toLowerCase()]["mahasiswa"] /
            data[event.target.value.toLowerCase()]["kuota"]) *
          100
        ).toFixed(1) > 100
          ? 0
          : 100 -
            (
              (data[event.target.value.toLowerCase()]["mahasiswa"] /
                data[event.target.value.toLowerCase()]["kuota"]) *
              100
            ).toFixed(1),
      ];

      document.getElementById("ratio").innerHTML = `${parseInt(
        data[event.target.value.toLowerCase()]["bimbingan"]
      )}`;

      document.getElementById("pemenuhan-number").innerHTML = `${(
        (data[event.target.value.toLowerCase()]["mahasiswa"] /
          data[event.target.value.toLowerCase()]["kuota"]) *
        100
      ).toFixed(1)} %`;
      document.getElementById("ratio").innerHTML = `${parseInt(
        data[event.target.value.toLowerCase()]["bimbingan"]
      )}`;

      myChart.update();
      chart.update();
    });
  });
