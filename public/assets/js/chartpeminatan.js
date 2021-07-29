// var myChart, chart;

// fetch("/api/bi/datapeminatan")
//   .then((res) => {
//     return res.json();
//   })
//   .then((data) => {
//     console.log(data);
//     if (data["EDE"] != null) {
//       document.getElementById("content").innerHTML = `
//       <div class="container">
//       <div class="row">
//         <div class="col-xl-4 col-md-12 col-sm-12 ml-auto">
//           <div class="row">
//             <div class="col">
//               <div class="card py-4 px-5">
//                 <div class="row">
//                   <div class="col">
//                     <h2>Pemenuhan Kuota</h2>
//                   </div>
//                 </div>
//                 <div class="row mt-3 py-4 p-relative">
//                   <p class="position-absolute middle" id="pemenuhan-number">
//                     50%
//                   </p>
//                   <canvas id="pemenuhan" height="200px"></canvas>
//                 </div>
//               </div>
//             </div>
//           </div>
//           <div class="row mt-4 mb-4">
//             <div class="col">
//               <div class="card py-4 px-5 position-relative">
//                 <div class="row">
//                   <div class="col">
//                     <h2>Rata-rata Mahasiswa Bimbingan Per Dosen</h2>
//                   </div>
//                 </div>
//                 <div class="row">
//                   <div class="col d-flex justify-content-center">
//                     <p id="ratio" class="medium"></p>
//                   </div>
//                 </div>
//               </div>
//             </div>
//           </div>
//         </div>
  
//         <div class="col-xl-4 col-md-12 col-sm 12 mr-auto">
//           <div class="card py-4 px-5" style="height: 39rem">
//             <div class="row">
//               <div class="col">
//                 <h2>Jumlah Mahasiswa Terhadap Kuota</h2>
//               </div>
//             </div>
//             <div class="row" style="height: 100%">
//               <div class="col" style="height: 100%">
//                 <canvas id="mahasiswakuota" height="100%"></canvas>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//       `;
//       var cta = document.getElementById("mahasiswakuota").getContext("2d");
//       var ctx = document.getElementById("pemenuhan");
//       myChart = new Chart(cta, {
//         type: "bar",
//         data: {
//           labels: ["EISD"],
//           datasets: [
//             {
//               label: "Mahasiswa",
//               borderRadius: 2,
//               data: [data["EISD"]["mahasiswa"]],
//               borderColor: "#2b73d7",
//               borderWidth: 2,
//               backgroundColor: "#2b73d783",
//               fontColor: "white",
//             },
//             {
//               label: "Kuota",
//               tension: 0,
//               borderColor: "#FF6384",
//               borderWidth: 2,
//               backgroundColor: "#ff638583",
//               data: [data["EISD"]["kuota"]],
//             },
//           ],
//         },
//         options: {
//           maintainAspectRatio: false,
//           legend: {
//             display: true,
//             position: "bottom",
//             labels: {
//               fontColor: "#8898AA",
//             },
//           },
//           scales: {
//             yAxes: [
//               {
//                 gridLines: {
//                   display: true,
//                 },
//                 ticks: {
//                   beginAtZero: true,
//                   max:
//                     data["EISD"]["kuota"] > data["EISD"]["mahasiswa"]
//                       ? data["EISD"]["kuota"]
//                       : data["EISD"]["mahasiswa"],
//                 },
//               },
//             ],
//             xAxes: [
//               {
//                 stacked: true,
//                 gridLines: {
//                   display: false,
//                 },
//                 ticks: {
//                   fontColor: "black",
//                 },
//               },
//             ],
//           },

//           tooltips: {
//             enabled: true,
//             mode: "index",
//             intersect: true,
//           },
//         },
//       });

//       chart = new Chart(ctx, {
//         type: "doughnut",
//         data: {
//           labels: ["Terisi", "Kosong"],
//           datasets: [
//             {
//               label: "Gauge",
//               data: [
//                 (
//                   (data["EISD"]["mahasiswa"] / data["EISD"]["kuota"]) *
//                   100
//                 ).toFixed(1) > 100
//                   ? 100
//                   : (
//                       (data["EISD"]["mahasiswa"] / data["EISD"]["kuota"]) *
//                       100
//                     ).toFixed(1),
//                 (
//                   (data["EISD"]["mahasiswa"] / data["EISD"]["kuota"]) *
//                   100
//                 ).toFixed(1) > 100
//                   ? 0
//                   : 100 -
//                     (
//                       (data["EISD"]["mahasiswa"] / data["EISD"]["kuota"]) *
//                       100
//                     ).toFixed(1),
//               ],
//               backgroundColor: ["rgb(54, 162, 235)", "rgb(255, 99, 132)"],
//             },
//           ],
//         },
//         options: {
//           tooltips: {
//             callbacks: {
//               label: function (tooltipItem, data) {
//                 var dataset = data.datasets[tooltipItem.datasetIndex];
//                 var meta = dataset._meta[Object.keys(dataset._meta)[0]];
//                 var total = meta.total;
//                 var currentValue = dataset.data[tooltipItem.index];
//                 var percentage = parseFloat(
//                   ((currentValue / total) * 100).toFixed(1)
//                 );
//                 return currentValue + " (" + percentage + "%)";
//               },
//               title: function (tooltipItem, data) {
//                 return data.labels[tooltipItem[0].index];
//               },
//             },
//           },
//           responsive: true,
//           maintainAspectRatio: false,
//           legend: {
//             display: false,
//           },
//         },
//       });

//       document.getElementById("pemenuhan-number").innerHTML = `${(
//         (data["EISD"]["mahasiswa"] / data["EISD"]["kuota"]) *
//         100
//       ).toFixed(1)} %`;
//       document.getElementById("ratio").innerHTML = `${parseInt(
//         data["EISD"]["bimbingan"]
//       )}`;

//       document
//         .getElementById("peminatan")
//         .addEventListener("change", (event) => {
//           myChart.data.datasets[0].data = [
//             data[event.target.value]["mahasiswa"],
//           ];
//           myChart.data.datasets[1].data = [data[event.target.value]["kuota"]];
//           myChart.options.scales.yAxes[0].ticks.max =
//             data[event.target.value]["kuota"] >
//             data[event.target.value]["mahasiswa"]
//               ? data[event.target.value]["kuota"]
//               : data[event.target.value]["mahasiswa"];

//           chart.data.datasets[0].data = [
//             (
//               (data[event.target.value]["mahasiswa"] /
//                 data[event.target.value]["kuota"]) *
//               100
//             ).toFixed(1) > 100
//               ? 100
//               : (
//                   (data[event.target.value]["mahasiswa"] /
//                     data[event.target.value]["kuota"]) *
//                   100
//                 ).toFixed(1),
//             (
//               (data[event.target.value]["mahasiswa"] /
//                 data[event.target.value]["kuota"]) *
//               100
//             ).toFixed(1) > 100
//               ? 0
//               : 100 -
//                 (
//                   (data[event.target.value]["mahasiswa"] /
//                     data[event.target.value]["kuota"]) *
//                   100
//                 ).toFixed(1),
//           ];

//           document.getElementById("ratio").innerHTML = `${parseInt(
//             data[event.target.value]["bimbingan"]
//           )}`;

//           document.getElementById("pemenuhan-number").innerHTML = `${(
//             (data[event.target.value]["mahasiswa"] /
//               data[event.target.value]["kuota"]) *
//             100
//           ).toFixed(1)} %`;
//           document.getElementById("ratio").innerHTML = `${parseInt(
//             data[event.target.value]["bimbingan"]
//           )}`;

//           myChart.update();
//           chart.update();
//         });
//     } else {
//       document.getElementById("content").innerHTML = `
//       <div class="row mt-5">
//       <div class="col">
//         <h3 class="text-center">Belum ada data.</h3>
//       </div>
//     </div>
//   `;
//     }
//   });
