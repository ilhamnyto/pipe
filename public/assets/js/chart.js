var charta, chartb, chartc, chartd, charte, chartf;

fetch("/api/bi/overall")
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    if (Object.keys(data).length) {
      document.getElementById("content").innerHTML = `
      <div class="row mb-1">
      <div class="col-md-2 ml-auto">
        <div class="form-group d-inline mr-3">
          <select
            name="angkatan"
            id="angkatan-select"
            class="form-select pr-5"
          ></select>
        </div>
      </div>
    </div>
    <div class="row mb-2">
      <div class="col-xl-6 col-md-12 col-sm-12">
        <div class="row">
          <div class="col">
            <div class="card py-2">
              <span class="text-center font-weight-bold">MAHASISWA</span>
            </div>
          </div>
        </div>
  
        <div class="row mt-2">
          <div class="col-xl-3 col-md-12 col-sm-12">
            <div class="row mb-2">
              <div class="col">
                <div class="card p-4" style="min-height: 9.7rem">
                  <div class="row">
                    <div class="col">
                      <p
                        class="font-weight-bold text-center"
                        style="font-size: 0.8rem"
                      >
                        Total Mahasiswa
                      </p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col">
                      <p
                        class="h1 text-center mt-2 font-weight-bold"
                        id="total-mahasiswa"
                      >
                        340
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <div class="card p-4" style="min-height: 9.7rem">
                  <div class="row">
                    <div class="col">
                      <p
                        class="font-weight-bold text-center"
                        style="font-size: 0.8rem"
                      >
                        Kuota Tersedia
                      </p>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col">
                      <p
                        class="h1 text-center mt-2 font-weight-bold"
                        id="kuota-tersedia"
                      >
                        450
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col mt-xl-0">
            <div class="card p-3" style="min-height: 20rem">
              <div class="row">
                <div class="col">
                  <p class="text-center font-weight-bold" style="font-size: 1rem">
                    Perbandingan Mahasiswa Dengan Kuota Peminatan
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col-xl-10 mx-auto">
                  <canvas id="kuotamahasiswa" width="490px"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <div class="col-xl-6 col-md-12 col-sm-12">
        <div class="row mb-2">
          <div class="col">
            <div class="card py-2">
              <span class="text-center font-weight-bold">DOSEN</span>
            </div>
          </div>
        </div>
  
        <div class="row">
          <div class="col-xl-4">
            <div class="card p-2" style="min-height: 20rem">
              <div class="row">
                <div class="col">
                  <p
                    class="text-center font-weight-bold mt-4"
                    style="font-size: 1rem; margin-bottom: -1rem"
                  >
                    Dosen Kelompok<br/> Keahlian
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col mx-auto">
                  <canvas id="kelompokkeahlian" width="480px"></canvas>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-4">
            <div class="card p-2" style="min-height: 20rem">
              <div class="row">
                <div class="col">
                  <p
                    class="text-center font-weight-bold mt-4"
                    style="font-size: 1rem; margin-bottom: -1rem"
                  >
                    Dosen Peminatan
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col mx-auto">
                  <canvas id="dosenpeminatan" width="490px"></canvas>
                </div>
              </div>
            </div>
          </div>
          <div class="col-xl-4">
            <div class="card p-2" style="min-height: 20rem">
              <div class="row">
                <div class="col">
                  <p
                    class="text-center font-weight-bold mt-4"
                    style="font-size: 1rem; margin-bottom: -0.2rem"
                  >
                    Rata-rata Mahasiswa Bimbingan
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col mx-auto">
                  <canvas id="bimbingan" width="450px"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <div class="row mb-2">
      <div class="col">
        <div class="card py-2">
          <span class="text-center font-weight-bold"
            >HASIL SELEKSI PEMINATAN</span
          >
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="card p-2" style="min-height: 20rem">
          <div class="row mt-3">
            <div class="col">
              <p class="text-center font-weight-bold" style="font-size: 1rem">
                Trend Kelompok Keahlian
              </p>
            </div>
          </div>
          <div class="row">
            <div class="col mx-auto">
              <canvas id="trendkeahlian" width="500px"></canvas>
            </div>
          </div>
        </div>
      </div>
  
      <div class="col">
        <div class="card p-2" style="min-height: 20rem">
          <div class="row mt-3">
            <div class="col">
              <p class="text-center font-weight-bold" style="font-size: 1rem">
                Trend Peminatan
              </p>
            </div>
          </div>
          <div class="row">
            <div class="col mx-auto">
              <canvas id="trendpeminatan" width="500px"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
      `;

      var cta = document.getElementById("kuotamahasiswa").getContext("2d");
      var ctb = document.getElementById("kelompokkeahlian").getContext("2d");
      var ctc = document.getElementById("dosenpeminatan").getContext("2d");
      var ctd = document.getElementById("bimbingan").getContext("2d");
      var cte = document.getElementById("trendkeahlian").getContext("2d");
      var ctf = document.getElementById("trendpeminatan").getContext("2d");

      Object.keys(data)
        .reverse()
        .forEach((el) => {
          document.getElementById(
            "angkatan-select"
          ).innerHTML += `<option value="${el}">${el}</option>`;
        });

      document.getElementById("total-mahasiswa").innerHTML = Object.values(
        Object.values(data).reverse()[0]
      ).reduce((total, val) => {
        return total + val["mahasiswa"];
      }, 0);

      document.getElementById("kuota-tersedia").innerHTML = Object.values(
        Object.values(data).reverse()[0]
      ).reduce((total, val) => {
        return total + val["kuota"];
      }, 0);

      charta = new Chart(cta, {
        plugins: [ChartDataLabels],
        type: "bar",
        data: {
          labels: ["EDE", "EIM", "EISD", "ERP", "SAG"],
          datasets: [
            {
              label: ["Mahasiswa"],
              fill: false,
              backgroundColor: "#0A9396",
              data: Object.values(Object.values(data).reverse()[0]).map(
                (el) => el["mahasiswa"]
              ),
              datalabels: {},
            },
            {
              label: ["Kuota Peminatan"],
              fill: false,
              backgroundColor: "#005F73",
              data: Object.values(Object.values(data).reverse()[0]).map(
                (el) => el["kuota"]
              ),
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
                size: 10,
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
                  display: true,
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

      chartb = new Chart(ctb, {
        type: "pie",
        data: {
          labels: ["Cybernetics", "EINS"],
          datasets: [
            {
              data: [
                Object.values(Object.values(data).reverse()[0]).reduce(
                  (total, val) => {
                    if (val["keahlian"] == "CYBERNETICS") {
                      return total + val["dosen"];
                    }
                    return total + 0;
                  },
                  0
                ),
                Object.values(Object.values(data).reverse()[0]).reduce(
                  (total, val) => {
                    if (val["keahlian"] == "EINS") {
                      return total + val["dosen"];
                    }
                    return total + 0;
                  },
                  0
                ),
              ],
              backgroundColor: ["#EE6C4D", "#EE9B00"],
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
          title: {
            display: true,
            align: "end",
          },
          legend: {
            position: "bottom",
            labels: {
              boxWidth: 12,
            },
          },
        },
      });

      chartc = new Chart(ctc, {
        type: "pie",
        data: {
          labels: ["EDE", "EIM", "EISD", "ERP", "SAG"],
          datasets: [
            {
              data: [
                Object.values(Object.values(data).reverse()[0])[0]["dosen"],
                Object.values(Object.values(data).reverse()[0])[1]["dosen"],
                Object.values(Object.values(data).reverse()[0])[2]["dosen"],
                Object.values(Object.values(data).reverse()[0])[3]["dosen"],
                Object.values(Object.values(data).reverse()[0])[4]["dosen"],
              ],
              backgroundColor: [
                "#ef476f",
                "#ffd166",
                "#06d6a0",
                "#118ab2",
                "#073b4c",
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
          title: {
            display: true,
            align: "end",
          },
          legend: {
            position: "bottom",
            labels: {
              boxWidth: 12,
            },
          },
        },
      });

      chartd = new Chart(ctd, {
        plugins: [ChartDataLabels],
        type: "bar",
        data: {
          labels: ["Cybernetics", "EINS"],
          datasets: [
            {
              label: ["Mahasiswa"],
              data: [
                (
                  Object.values(Object.values(data).reverse()[0]).reduce(
                    (total, val) => {
                      if (val["keahlian"] == "CYBERNETICS") {
                        return total + val["mahasiswa"];
                      }
                      return total + 0;
                    },
                    0
                  ) /
                  Object.values(Object.values(data).reverse()[0]).reduce(
                    (total, val) => {
                      if (val["keahlian"] == "CYBERNETICS") {
                        return total + val["dosen"];
                      }
                      return total + 0;
                    },
                    0
                  )
                ).toFixed(1),
                (
                  Object.values(Object.values(data).reverse()[0]).reduce(
                    (total, val) => {
                      if (val["keahlian"] == "EINS") {
                        return total + val["mahasiswa"];
                      }
                      return total + 0;
                    },
                    0
                  ) /
                  Object.values(Object.values(data).reverse()[0]).reduce(
                    (total, val) => {
                      if (val["keahlian"] == "EINS") {
                        return total + val["dosen"];
                      }
                      return total + 0;
                    },
                    0
                  )
                ).toFixed(1),
              ],
              datalabels: {},
              backgroundColor: ["#008C8F", "#008C8F"],
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
                size: 10,
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
                  display: true,
                  offsetGridLines: true,
                },
                ticks: {
                  display: true,
                  beginAtZero: true,
                  stepSize: 2,
                },
              },
            ],
            xAxes: [
              {
                stacked: false,
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

      charte = new Chart(cte, {
        plugins: [ChartDataLabels],
        type: "bar",
        data: {
          labels: ["2015", "2016", "2017"],
          datasets: [
            {
              label: "Cybernetics",
              borderRadius: 2,
              data: [
                Object.values(Object.values(data)[0]).reduce((total, val) => {
                  if (val["keahlian"] == "CYBERNETICS") {
                    return total + val["mahasiswa"];
                  }
                  return total + 0;
                }, 0),
                Object.values(Object.values(data)[1]).reduce((total, val) => {
                  if (val["keahlian"] == "CYBERNETICS") {
                    return total + val["mahasiswa"];
                  }
                  return total + 0;
                }, 0),
                Object.values(Object.values(data)[2]).reduce((total, val) => {
                  if (val["keahlian"] == "CYBERNETICS") {
                    return total + val["mahasiswa"];
                  }
                  return total + 0;
                }, 0),
              ],
              borderColor: "#EE6C4D",
              backgroundColor: "#EE6C4D",
              fontColor: "white",
              tension: 0,
              datalabels: {
                align: "end",
                anchor: "end",
              },
            },
            {
              label: "EINS",
              borderRadius: 2,
              data: [
                Object.values(Object.values(data)[0]).reduce((total, val) => {
                  if (val["keahlian"] == "EINS") {
                    return total + val["mahasiswa"];
                  }
                  return total + 0;
                }, 0),
                Object.values(Object.values(data)[1]).reduce((total, val) => {
                  if (val["keahlian"] == "EINS") {
                    return total + val["mahasiswa"];
                  }
                  return total + 0;
                }, 0),
                Object.values(Object.values(data)[2]).reduce((total, val) => {
                  if (val["keahlian"] == "EINS") {
                    return total + val["mahasiswa"];
                  }
                  return total + 0;
                }, 0),
              ],
              borderColor: "#EE9B00",
              backgroundColor: "#EE9B00",
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
                size: 10,
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

      chartf = new Chart(ctf, {
        plugins: [ChartDataLabels],
        type: "bar",
        data: {
          labels: ["2015", "2016", "2017"],
          datasets: [
            {
              label: ["EDE"],
              data: [
                Object.values(Object.values(data)[0])[0]["mahasiswa"],
                Object.values(Object.values(data)[1])[0]["mahasiswa"],
                Object.values(Object.values(data)[2])[0]["mahasiswa"],
              ],
              backgroundColor: ["#ef476f", "#ef476f", "#ef476f"],
              datalabels: {
                align: "end",
                anchor: "end",
              },
            },
            {
              label: ["EIM"],
              data: [
                Object.values(Object.values(data)[0])[1]["mahasiswa"],
                Object.values(Object.values(data)[1])[1]["mahasiswa"],
                Object.values(Object.values(data)[2])[1]["mahasiswa"],
              ],
              backgroundColor: ["#ffd166", "#ffd166", "#ffd166"],
              datalabels: {
                align: "end",
                anchor: "end",
              },
            },
            {
              label: ["EISD"],
              data: [
                Object.values(Object.values(data)[0])[2]["mahasiswa"],
                Object.values(Object.values(data)[1])[2]["mahasiswa"],
                Object.values(Object.values(data)[2])[2]["mahasiswa"],
              ],
              backgroundColor: ["#06d6a0", "#06d6a0", "#06d6a0"],
              datalabels: {
                align: "end",
                anchor: "end",
              },
            },
            {
              label: ["ERP"],
              data: [
                Object.values(Object.values(data).reverse()[0])[3]["mahasiswa"],
                Object.values(Object.values(data).reverse()[1])[3]["mahasiswa"],
                Object.values(Object.values(data).reverse()[2])[3]["mahasiswa"],
              ],
              backgroundColor: ["#118ab2", "#118ab2", "#118ab2"],
              datalabels: {
                align: "end",
                anchor: "end",
              },
            },
            {
              label: ["SAG"],
              data: [
                Object.values(Object.values(data).reverse()[0])[4]["mahasiswa"],
                Object.values(Object.values(data).reverse()[1])[4]["mahasiswa"],
                Object.values(Object.values(data).reverse()[2])[4]["mahasiswa"],
              ],
              backgroundColor: ["#073b4c", "#073b4c", "#073b4c"],
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
                size: 10,
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
      console.log(data);

      document
        .getElementById("angkatan-select")
        .addEventListener("change", (event) => {
          let tahun = event.target.value;

          document.getElementById("total-mahasiswa").innerHTML = Object.values(
            data[tahun]
          ).reduce((total, val) => {
            return total + val["mahasiswa"];
          }, 0);

          document.getElementById("kuota-tersedia").innerHTML = Object.values(
            data[tahun]
          ).reduce((total, val) => {
            return total + val["kuota"];
          }, 0);

          charta.data.datasets[0].data = Object.values(data[tahun]).map(
            (el) => el["mahasiswa"]
          );

          charta.data.datasets[1].data = Object.values(data[tahun]).map(
            (el) => el["kuota"]
          );

          chartb.data.datasets[0].data = [
            Object.values(data[tahun]).reduce((total, val) => {
              if (val["keahlian"] == "CYBERNETICS") {
                return total + val["dosen"];
              }
              return total + 0;
            }, 0),
            Object.values(data[tahun]).reduce((total, val) => {
              if (val["keahlian"] == "EINS") {
                return total + val["dosen"];
              }
              return total + 0;
            }, 0),
          ];

          chartc.data.datasets[0].data = Object.values(data[tahun]).map(
            (el) => el["dosen"]
          );

          chartd.data.datasets[0].data = [
            (
              Object.values(data[tahun]).reduce((total, val) => {
                if (val["keahlian"] == "CYBERNETICS") {
                  return total + val["mahasiswa"];
                }
                return total + 0;
              }, 0) /
              Object.values(data[tahun]).reduce((total, val) => {
                if (val["keahlian"] == "CYBERNETICS") {
                  return total + val["dosen"];
                }
                return total + 0;
              }, 0)
            ).toFixed(1),
            (
              Object.values(data[tahun]).reduce((total, val) => {
                if (val["keahlian"] == "EINS") {
                  return total + val["mahasiswa"];
                }
                return total + 0;
              }, 0) /
              Object.values(data[tahun]).reduce((total, val) => {
                if (val["keahlian"] == "EINS") {
                  return total + val["dosen"];
                }
                return total + 0;
              }, 0)
            ).toFixed(1),
          ];

          charta.update();
          chartb.update();
          chartc.update();
          chartd.update();
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
