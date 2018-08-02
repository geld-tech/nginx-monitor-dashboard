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
                <b-col sm="12">
                    <div v-if="data" class="Chart__list">
                        <div class="Chart">
                            <status v-bind:metrics="data"></status>
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
