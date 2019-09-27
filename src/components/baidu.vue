<template></template>

<script>
import { BmlMarkerClusterer } from "vue-baidu-map";
export default {
  data() {
    return {
      markers: [],
      province: ""
    };
  },
  created() {
    for (let i = 0; i < 10; i++) {
      const position = {
        lng: Math.random() * 40 + 85,
        lat: Math.random() * 30 + 21
      };
      this.markers.push(position);
    }
  },
  methods: {
    locate_success(res) {
      this.province = res.addressComponent.province;
      this.$Message.success("您是山东省第1个哟");
    }
  },
  components: {
    BmlMarkerClusterer
  }
};
</script>

<style  scoped>
.map {
  width: 100%;
  height: 300px;
}
</style>