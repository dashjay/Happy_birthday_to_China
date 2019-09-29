<template>
  <div>
    <div class="echarts">
      <div style="height:400px;width:100%;padding-top: 50px" ref="myEchart"></div>
    </div>
    <Button @click="fighting" style="margin-top:10px" type="warning" size="large">我也要为祖国加油</Button>
    <div>
      <Button @click="flag_up" class="test">我要去升旗</Button>
    </div>
  </div>
</template>

<script>
import echarts from "echarts";
// import "../../node_modules/echarts/map/js/world.js";
import "../../node_modules/echarts/map/js/china.js"; // 引入中国地图数据
export default {
  name: "echars",
  props: ["userJson"],
  data() {
    return {
      title: "图表",
      placeholder: "用户名/电话",
      find: "2", //1显示新增按钮，2显示导入按钮，若不显示这两个按钮可以写0或者不写值
      chart: null,
      address: "",
      nums: []
    };
  },
  mounted() {
    this.getdata();
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    fighting() {
      var c = this.getCookie("up");
      if (c == "b2s=") {
        this.$Notice.error({
          title: "你已经为祖国点亮了地图",
          desc: "你已经为祖国点亮了地图,点击下方按钮前去升旗"
        });
      } else {
        this.location();
      }
    },
    // 获取当前用户的位置
    location() {
      var self = this;
      // 开始 定位
      var geolocation = new BMap.Geolocation();
      geolocation.getCurrentPosition(function(r) {
        console.log(r.point);
        var point = new BMap.Point(r.point.lng, r.point.lat);
        var gc = new BMap.Geocoder();
        gc.getLocation(point, function(rs) {
          var addComp = rs.addressComponents;
          console.log(rs.address); //地址信息
          self.address = rs.address;
          self.submit();
          self.setCookie("up", "b2s=", 10);
        });
      });
    },
    submit() {
      let dataform = new FormData();
      dataform.append("addr", this.address);
      this.$http
        .post("/position", dataform)
        .then(response => {
          if (response.data.status) {
            let info = response.data;
            let c =
              "您是" +
              info.province +
              "的第" +
              info.rank +
              "位点亮地图的人 <br> 同时也是全国第" +
              info.total +
              "位点亮地图的人";
            this.$Modal.success({
              title: "成功为祖国加油",
              content: c
            });
          } else {
            this.$Modal.warning({
              title: "Fail",
              content: response.data.msg
            });
          }
        })
        .catch(error => {
          this.$Modal.warning({
            title: "Fail",
            content: error
          });
        });
    },
    getdata() {
      this.$http
        .get("/distribution")
        .then(response => {
          if (response.data.status) {
            this.nums = response.data.data;
            this.chinaConfigure();
          } else {
            this.chinaConfigure();
          }
        })
        .catch(error => {
          this.chinaConfigure();
        });
    },
    chinaConfigure() {
      let myChart = echarts.init(this.$refs.myEchart); //这里是为了获得容器所在位置
      window.onresize = myChart.resize;
      myChart.setOption({
        title: {
          // text: "分部图"
        },
        // 进行相关配置
        // backgroundColor: "#EF5858",
        //  backgroundColor: "#02AFDB",
        tooltip: {}, // 鼠标移到图里面的浮动提示框
        dataRange: {
          show: false,
          min: 200,
          max: 1000,
          text: ["High", "Low"],
          realtime: true,
          calculable: true,
          color: ["red"]
        },
        geo: {
          // 这个是重点配置区
          map: "china", // 表示中国地图
          roam: true,
          label: {
            normal: {
              show: false, // 是否显示对应地名
              textStyle: {
                color: "rgba(0.1,0.1,0.1,0.4)"
              }
            }
          },
          itemStyle: {
            normal: {
              borderColor: "rgba(0, 0, 0, 0.2)"
            },
            emphasis: {
              areaColor: null,
              shadowOffsetX: 0,
              shadowOffsetY: 0,
              shadowBlur: 20,
              borderWidth: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          }
        },
        series: [
          {
            type: "scatter",
            coordinateSystem: "geo" // 对应上方配置
          },
          {
            name: "点亮人数", // 浮动框的标题
            type: "map",
            geoIndex: 0,
            data: this.nums
          }
        ]
      });
    },
    flag_up() {
      window.location.href = "/flag";
    },
    setCookie: function(cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
      var expires = "expires=" + d.toUTCString();
      console.info(cname + "=" + cvalue + "; " + expires);
      document.cookie = cname + "=" + cvalue + "; " + expires;
      console.info(document.cookie);
    },
    getCookie: function(cname) {
      var name = cname + "=";
      var ca = document.cookie.split(";");
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        console.log(c);
        while (c.charAt(0) == " ") c = c.substring(1);
        if (c.indexOf(name) != -1) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    }
  },
  computed: {}
};
</script>

<style scoped>
.echart {
  /* margin: 100px; */
}
.test {
  position: absolute;
  bottom: 10px;
  left: 40%;
}
</style>
