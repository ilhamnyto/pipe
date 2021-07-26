var chart, cchart, myChart;
// kelompok keahlian

fetch("/api/bi/overall")
  .then((res) => {
    return res.json();
  })
  .then((data) => {
    console.log(data);
    if (
      data["dosenpeminatan"]["EISD"] != null &&
      data["dosenkeahlian"]["CYBERNETICS"] != null &&
      data["kuotamahasiswa"]["EISD"] != null
    ) {
      document.getElementById("content").innerHTML = `
      <div class="row mb-4">
      <div class="col-xl-12 col-sm-12 col-md-12">
      <div class="row">
      <div class="col-xl-3">
      <div class="row mb-4">
      <div class="col">
      <div class="card min-height py-4 px-5">
      <div class="row">
      <div class="col">
      <div class="row">
      <div class="col">
      <h2>Dosen tiap Peminatan</h2>
      </div>
      </div>
      <div class="row">
      <div class="col">
      <canvas id="dosenpeminatan"></canvas>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      <div class="row">
      <div class="col">
      <div class="card min-height py-4 px-5">
      <div class="row">
      <div class="col">
      <div class="row">
      <div class="col">
      <h2>Dosen tiap Kelompok Keahlian</h2>
      </div>
      </div>
      <div class="row">
      <div class="col">
      <canvas id="kelompokkeahlian"></canvas>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      <div class="col-xl-9 my-4 my-xl-0">
      <div class="card p-4" style="height: 32.3rem">
      <div class="row">
      <div class="col">
      <h2>Perbandingan Jumlah Mahasiswa dengan Kuota Peminatan</h2>
      </div>
      </div>
      <div class="row" style="height: 100%">
      <div class="col px-5 py-3">
      <canvas id="mahasiswakuota" style="height: 100%"></canvas>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      </div>
      `;
      var cta = document.getElementById("mahasiswakuota").getContext("2d");
      var ctb = document.getElementById("kelompokkeahlian").getContext("2d");
      var ctc = document.getElementById("dosenpeminatan").getContext("2d");
      chart = new Chart(ctb, {
        type: "pie",
        data: {
          labels: Object.keys(data["dosenkeahlian"]),
          datasets: [
            {
              data: Object.values(data["dosenkeahlian"]),
              backgroundColor: ["#2B73D7", "#75A1DE"],
            },
          ],
        },
        options: {
          plugins: {
            labels: {
              render: "percentage",
              precision: 2,
            },
          },
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

      cchart = new Chart(ctc, {
        type: "pie",
        data: {
          labels: Object.keys(data["dosenpeminatan"]),
          datasets: [
            {
              data: Object.values(data["dosenpeminatan"]),
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
      myChart = new Chart(cta, {
        type: "bar",
        data: {
          labels: Object.keys(data["kuotamahasiswa"]),
          datasets: [
            {
              label: "Mahasiswa",
              borderRadius: 2,
              data: Object.values(data["kuotamahasiswa"]).map(
                (el) => el.mahasiswa
              ),
              borderColor: "#2b73d7",
              borderWidth: 2,
              backgroundColor: "#2b73d783",
              fontColor: "white",
            },
            {
              label: "Kuota Peminatan",
              tension: 0,
              borderColor: "#FF6384",
              borderWidth: 2,
              backgroundColor: "#ff638583",
              data: Object.values(data["kuotamahasiswa"]).map((el) => el.kuota),
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
    } else {
      console.log("gaada");
      document.getElementById("content").innerHTML = `
          <div class="row mt-5">
          <div class="col">
            <h3 class="text-center">Belum ada data.</h3>
          </div>
        </div>
      `;
    }
  });
