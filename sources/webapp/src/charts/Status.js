import {Line} from 'vue-chartjs'

var chartColors = {
  red: 'rgb(255, 99, 132)',
  orange: 'rgb(255, 159, 64)',
  yellow: 'rgb(255, 205, 86)',
  green: 'rgb(75, 192, 192)',
  blue: 'rgb(54, 162, 235)',
  purple: 'rgb(153, 102, 255)',
  grey: 'rgb(231,233,237)'
}

export default {
  extends: Line,
  props: ['metrics'],
  mounted () {
    this.renderLinesChart()
  },
  computed: {
    linesChartData: function() {
      return this.metrics
    },
    datetimeLabels: function() {
      var labels = []
      for (var i = 0; i < this.metrics.length; ++i) {
        labels.push(this.metrics[i].date_time)
      }
      return labels
    },
    active: function() {
      var active = []
      for (var i = 0; i < this.metrics.length; ++i) {
        active.push(this.metrics[i].active)
      }
      return active
    },
    writing: function() {
      var writing = []
      for (var i = 0; i < this.metrics.length; ++i) {
        writing.push(this.metrics[i].writing)
      }
      return writing
    },
    reading: function() {
      var reading = []
      for (var i = 0; i < this.metrics.length; ++i) {
        reading.push(this.metrics[i].reading)
      }
      return reading
    },
    waiting: function() {
      var waiting = []
      for (var i = 0; i < this.metrics.length; ++i) {
        waiting.push(this.metrics[i].waiting)
      }
      return waiting
    }
  },
  methods: {
    renderLinesChart: function() {
      this.renderChart({
        labels: this.datetimeLabels,
        datasets: [
          {
            label: 'Active',
            fill: false,
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: this.active
          },
          {
            label: 'Writing',
            fill: false,
            backgroundColor: chartColors.yellow,
            borderColor: chartColors.yellow,
            data: this.writing
          },
          {
            label: 'Reading',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: this.reading
          },
          {
            label: 'Waiting',
            fill: false,
            backgroundColor: chartColors.grey,
            borderColor: chartColors.grey,
            data: this.waiting
          }
        ]
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        elements: {
          point: {
            radius: 0
          }
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: false
            }
          }],
          yAxes: [{
            stacked: false,
            ticks: {
              beginAtZero: true,
              stepSize: 1
            },
            scaleLabel: {
              display: true,
              labelString: 'Count'
            }
          }]
        }
      })
    }
  },
  watch: {
    metrics: function() {
      this.$data._chart.destroy()
      this.renderLinesChart()
    }
  }
}
