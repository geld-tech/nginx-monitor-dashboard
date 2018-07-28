<template>
  <div class="index">
    <!-- Container -->
    <b-container class="bv-example-row">
        <div v-if="Object.keys(data).length === 0" class="loading">
            <h6>Loading...</h6>
            <img src="/static/images/spinner.gif" width="32" height="32"/>
        </div>
        <div v-else>
            <h3>{{ msg }}</h3>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h5>Hostname</h5>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ data.hostname }}</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h5>Uptime</h5>
                </b-col>
                <b-col sm="8">
                    <p v-if="data">{{ parseInt(data.uptime/60/60/24) }} days</p>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h5>CPU</h5>
                </b-col>
                <b-col sm="8">
                    <b-progress show-progress v-if="data && data.cpu_percent !== undefined" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="primary" v-bind:value="data.cpu_percent" v-bind:label="data.cpu_percent.toFixed(1)+'%' || '0'" height="20px"></b-progress-bar>
                    </b-progress>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h5>Memory</h5>
                </b-col>
                <b-col sm="8">
                    <b-progress show-progress v-if="data && data.vmem_percent !== undefined" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="primary" v-bind:value="data.vmem_percent" v-bind:label="data.vmem_percent.toFixed(1)+'%' || '0'" height="20px"></b-progress-bar>
                    </b-progress>
                    <b-progress show-progress v-if="data && data.swap_usage !== undefined && data.swap_usage['percent'] > 1" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="warning" v-bind:value="data.swap_usage['percent']"
                            v-bind:label="data.swap_usage['percent'].toFixed(1)+'%' || '0'" height="20px">
                        </b-progress-bar>
                    </b-progress>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h5>Temperature</h5>
                </b-col>
                <b-col sm="8">
                    <b-progress show-progress v-if="data && data.cpu_temp !== false" v-bind:max="100" class="w-80 mb-2">
                        <b-progress-bar variant="primary" v-bind:value="data.cpu_temp" v-bind:label="data.cpu_temp+'&deg; C'" height="20px"></b-progress-bar>
                    </b-progress>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <h5>Disks</h5>
                </b-col>
                <b-col sm="8">
                    <div v-if="data && data.disks_usage" v-for="disk in data.disks_usage" v-bind:key="disk">
                        <b-progress show-progress v-if="disk['mountpoint']" v-bind:max="100" class="w-80 mb-2">
                            <b-progress-bar variant="primary" v-bind:value="disk['percent']" v-bind:label="disk['mountpoint']+' '+disk['percent']+'%'" height="20px"></b-progress-bar>
                        </b-progress>
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="4">
                    <b-btn v-b-toggle.processesText class="mb-3">Processes</b-btn>
                </b-col>
                <b-col sm="8">
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <div v-if="data">
                    <b-collapse id="processesText">
                      <b-card>
                          <b-table striped hover class="processesTable"
                            v-bind:items="data.processes"
                            v-bind:fields="[{key:'pid',sortable:true}, {key:'name',sortable:true}, {key:'cpu_percent',sortable:true,sortDirection:'desc'}]"
                            v-bind:per-page="12">
                        </b-table>
                      </b-card>
                    </b-collapse>
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <div v-if="data" class="Chart__list">
                        <div class="Chart">
                            <status v-bind:graphs_data="data.graphs_data"></status>
                        </div>
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <hr />
                </b-col>
            </b-row>
        </div>
    </b-container>
  </div>
</template>

<script>
import Status from './charts/Status.js'

export default {
  name: 'Info',
  props: ['loading', 'data'],
  components: {
    Status
  },
  data () {
    return {
      msg: 'Resources'
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.processesTable{
  font-size: 14px;
}
.container {
  max-width: 800px;
  margin:  0 auto;
}
.Chart {
  background: #FFFFFF;
}
.Chart h2 {
  margin-top: 0;
  padding: 15px 0;
  border-bottom: 1px solid #323d54;
}
</style>
