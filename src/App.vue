<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import $ from "jquery";
export default {
  name: "App",
  methods: {
    fighting() {
      var self = this;
      $.ajax({
        url:
          "http://api.map.baidu.com/location/ip?ak=ekuUwutrDTvW6dtwzG35XIn5N2i5LRqe",
        type: "GET",
        dataType: "JSONP",
        success: function(res) {
          // self.data = res.result;
          console.log(res);
        }
      });
    }
  },
  created() {}
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
