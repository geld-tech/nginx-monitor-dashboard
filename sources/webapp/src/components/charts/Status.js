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
  props: ['graphs_data'],
  mounted () {
    this.renderLinesChart()
  },
  computed: {
    linesChartData: function() {
      return this.graphs_data
    }
  },
  methods: {
    renderLinesChart: function() {
      this.renderChart({
        labels: this.linesChartData.date_time,
        datasets: [
          {
            label: 'CPU',
            fill: false,
            backgroundColor: chartColors.red,
            borderColor: chartColors.red,
            data: this.linesChartData.cpu_percent
          },
          {
            label: 'Memory',
            fill: false,
            backgroundColor: chartColors.blue,
            borderColor: chartColors.blue,
            data: this.linesChartData.vmem_percent
          }
        ]
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        animation: false
      })
    }
  },
  watch: {
    graphs_data: function() {
      this.$data._chart.destroy()
      this.renderLinesChart()
    }
  }
}
