var ctb = document.getElementById("matakuliah").getContext("2d");
var ctc = document.getElementById("lulus").getContext("2d");
var myChart, chart;

fetch("/api/bi/datanilai")
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    myChart = new Chart(ctb, {
      type: "pie",
      data: {
        labels: ["A", "AB", "B", "BC", "C", "D", "E"],
        datasets: [
          {
            data: Object.values(data["all"]),
            backgroundColor: [
              "#3A9278",
              "#43aa8b",
              "#90be6d",
              "#f9c74f",
              "#f8961e",
              "#f3722c",
              "#f94144",
            ],
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
          position: "left",
          labels: {
            boxWidth: 12,
          },
        },
      },
    });

    chart = new Chart(ctc, {
      type: "pie",
      data: {
        labels: ["Mengulang", "Tidak Mengulang"],
        datasets: [
          {
            data: [
              data["all"]["E"],
              data["all"]["A"] +
                data["all"]["AB"] +
                data["all"]["B"] +
                data["all"]["BC"] +
                data["all"]["C"] +
                data["all"]["D"],
            ],
            backgroundColor: ["rgb(255, 99, 132)", "#2B73D7"],
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

    document.getElementById("matkul").addEventListener("change", (event) => {
      myChart.data.datasets[0].data = Object.values(
        data[event.target.value.toLowerCase()]
      );

      chart.data.datasets[0].data = [
        data[event.target.value.toLowerCase()]["E"],
        data[event.target.value.toLowerCase()]["A"] +
          data[event.target.value.toLowerCase()]["AB"] +
          data[event.target.value.toLowerCase()]["B"] +
          data[event.target.value.toLowerCase()]["BC"] +
          data[event.target.value.toLowerCase()]["C"] +
          data[event.target.value.toLowerCase()]["D"],
      ];

      myChart.update();
      chart.update();
    });
  });
