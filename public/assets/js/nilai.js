var myChart, chart, chartcc;

fetch("/api/bi/datanilai")
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    if (Object.keys(data).length) {
      document.getElementById("content").innerHTML = `
      <div class="row mb-3">
  <div class="col-xl-5 ml-auto d-flex justify-content-end">
    <div class="form-group d-inline mr-3">
      <select name="angkatan" id="angkatan-select" class="form-select pr-5">
      </select>
    </div>
    <div class="form-group d-inline">
      <select name="matkul" id="matkul-select" class="form-select pr-5">
      </select>
    </div>
  </div>
</div>
<!-- peminatan -->

<div class="row">
  <div class="col">
    <div class="card py-2">
      <span class="text-center font-weight-bold">PERFORMA MAHASISWA</span>
    </div>
  </div>
</div>

<div class="row mt-2">
  <div class="col-xl-4">
    <div class="card p-2 pb-4" style="min-height: 20rem">
      <div class="row">
        <div class="col d-flex justify-content-center mt-3">
          <span class="text-center h5" style="font-weight: 600"
            >Nilai Mata Kuliah</span
          >
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-xl-10 mx-auto">
          <canvas id="matakuliah" width="500px"></canvas>
        </div>
      </div>
    </div>
  </div>
  <div class="col-xl-4">
    <div class="card p-2 pb-4" style="min-height: 20rem">
      <div class="row">
        <div class="col d-flex justify-content-center mt-3">
          <span class="text-center h5" style="font-weight: 600"
            >Mahasiswa Mengulang</span
          >
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-xl-10 mx-auto">
          <canvas id="lulus" width="500px"></canvas>
        </div>
      </div>
    </div>
  </div>
  <div class="col-xl-4">
    <div class="card p-2 pb-4" style="min-height: 20rem">
      <div class="row">
        <div class="col d-flex justify-content-center mt-3">
          <span class="text-center h5" style="font-weight: 600"
            >Trend Mahasiswa Mengulang</span
          >
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-xl-10 mx-auto">
          <canvas id="trendlulus" width="500px"></canvas>
        </div>
      </div>
    </div>
  </div>
</div>
      `;
      Object.keys(data)
        .reverse()
        .forEach((el) => {
          document.getElementById(
            "angkatan-select"
          ).innerHTML += `<option value="${el}">${el}</option>`;
        });
      Object.values(data)
        .reverse()[0]
        .forEach((el) => {
          document.getElementById(
            "matkul-select"
          ).innerHTML += `<option value="${el.matkulid}">${el.matkulid}</option>`;
        });

      var ctb = document.getElementById("matakuliah").getContext("2d");
      var ctc = document.getElementById("lulus").getContext("2d");
      var ctd = document.getElementById("trendlulus").getContext("2d");

      myChart = new Chart(ctb, {
        type: "pie",
        data: {
          labels: ["A", "AB", "B", "BC", "C", "D", "E"],
          datasets: [
            {
              data: Object.values(Object.values(data).reverse()[0][0]).filter(
                (el) => typeof el === "number"
              ),
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
          tooltips: {
            callbacks: {
              label: function (tooltipItem, data) {
                var dataset = data.datasets[tooltipItem.datasetIndex];
                var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                var total = meta.total;
                var currentValue = dataset.data[tooltipItem.index];
                var percentage = parseFloat(
                  ((currentValue / total) * 100).toFixed(1)
                );
                return currentValue + " (" + percentage + "%)";
              },
              title: function (tooltipItem, data) {
                return data.labels[tooltipItem[0].index];
              },
            },
          },
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            arc: {
              borderWidth: 0.5,
            },
          },
          legend: {
            position: "right",
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
                Object.values(data).reverse()[0][0]["E"],
                Object.values(data).reverse()[0][0]["A"] +
                  Object.values(data).reverse()[0][0]["AB"] +
                  Object.values(data).reverse()[0][0]["B"] +
                  Object.values(data).reverse()[0][0]["BC"] +
                  Object.values(data).reverse()[0][0]["C"] +
                  Object.values(data).reverse()[0][0]["D"],
              ],
              backgroundColor: ["#f94144", "#3A9278"],
            },
          ],
        },
        options: {
          tooltips: {
            callbacks: {
              label: function (tooltipItem, data) {
                var dataset = data.datasets[tooltipItem.datasetIndex];
                var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                var total = meta.total;
                var currentValue = dataset.data[tooltipItem.index];
                var percentage = parseFloat(
                  ((currentValue / total) * 100).toFixed(1)
                );
                return currentValue + " (" + percentage + "%)";
              },
              title: function (tooltipItem, data) {
                return data.labels[tooltipItem[0].index];
              },
            },
          },
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            arc: {
              borderWidth: 0.5,
            },
          },
          legend: {
            position: "right",
            labels: {
              boxWidth: 12,
            },
          },
        },
      });

      chartcc = new Chart(ctd, {
        plugins: [ChartDataLabels],
        type: "bar",
        data: {
          labels: ["2015", "2016", "2017"],
          datasets: [
            {
              label: "Mengulang",
              borderRadius: 2,
              data: Object.values(data).map((el) => {
                return el[0]["E"];
              }),
              borderColor: "#ef476f",
              backgroundColor: "#F94144",
              fill: false,
              fontColor: "white",
              tension: 0,
              datalabels: {
                align: "end",
                anchor: "end",
              },
            },
          ],
        },
        options: {
          plugins: {
            datalabels: {
              backgroundColor: function (context) {
                return context.dataset.backgroundColor;
              },
              borderRadius: 4,
              color: "white",
              font: {
                weight: "bold",
              },
              formatter: Math.round,
              padding: 6,
            },
          },

          maintainAspectRatio: false,
          legend: {
            display: true,
            position: "bottom",
            labels: {
              fontColor: "black",
            },
          },
          scales: {
            yAxes: [
              {
                gridLines: {
                  display: false,
                  offsetGridLines: true,
                },
                ticks: {
                  display: true,
                  beginAtZero: true,
                  max: 300,
                  stepSize: 50,
                },
              },
            ],
            xAxes: [
              {
                gridLines: {
                  display: true,
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

      document
        .getElementById("matkul-select")
        .addEventListener("change", (event) => {
          let year = document.getElementById("angkatan-select").value;

          myChart.data.datasets[0].data = Object.values(
            Object.values(data[year]).filter(
              (el) => el["matkulid"] == event.target.value
            )[0]
          ).filter((el) => typeof el === "number");

          chart.data.datasets[0].data = [
            Object.values(data[year]).filter(
              (el) => el["matkulid"] == event.target.value
            )[0]["E"],
            Object.values(data[year]).filter(
              (el) => el["matkulid"] == event.target.value
            )[0]["A"] +
              Object.values(data[year]).filter(
                (el) => el["matkulid"] == event.target.value
              )[0]["AB"] +
              Object.values(data[year]).filter(
                (el) => el["matkulid"] == event.target.value
              )[0]["B"] +
              Object.values(data[year]).filter(
                (el) => el["matkulid"] == event.target.value
              )[0]["BC"] +
              Object.values(data[year]).filter(
                (el) => el["matkulid"] == event.target.value
              )[0]["C"] +
              Object.values(data[year]).filter(
                (el) => el["matkulid"] == event.target.value
              )[0]["D"],
          ];

          chartcc.data.datasets[0].data = Object.values(data).map((el) => {
            return el.filter((el) => el.matkulid == event.target.value)[0]["E"];
          });

          myChart.update();
          chart.update();
          chartcc.update();
        });

      document
        .getElementById("angkatan-select")
        .addEventListener("change", (event) => {
          console.log(event.target.value);
          let matkul = document.getElementById("matkul-select").value;

          myChart.data.datasets[0].data = Object.values(
            Object.values(data[event.target.value]).filter(
              (el) => el["matkulid"] == matkul
            )[0]
          ).filter((el) => typeof el === "number");

          chart.data.datasets[0].data = [
            Object.values(data[event.target.value]).filter(
              (el) => el["matkulid"] == matkul
            )[0]["E"],
            Object.values(data[event.target.value]).filter(
              (el) => el["matkulid"] == matkul
            )[0]["A"] +
              Object.values(data[event.target.value]).filter(
                (el) => el["matkulid"] == matkul
              )[0]["AB"] +
              Object.values(data[event.target.value]).filter(
                (el) => el["matkulid"] == matkul
              )[0]["B"] +
              Object.values(data[event.target.value]).filter(
                (el) => el["matkulid"] == matkul
              )[0]["BC"] +
              Object.values(data[event.target.value]).filter(
                (el) => el["matkulid"] == matkul
              )[0]["C"] +
              Object.values(data[event.target.value]).filter(
                (el) => el["matkulid"] == matkul
              )[0]["D"],
          ];

          chartcc.data.datasets[0].data = Object.values(data).map((el) => {
            return el.filter((el) => el.matkulid == matkul)[0]["E"];
          });

          myChart.update();
          chart.update();
          chartcc.update();
        });
    } else {
      document.getElementById("content").innerHTML = `
          <div class="row mt-5">
          <div class="col">
            <h3 class="text-center" style="margin-top: 20rem;">Belum ada data.</h3>
          </div>
        </div>
      `;
    }
  });
