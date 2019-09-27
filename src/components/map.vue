<template>
  <div>
    <div class="echarts">
      <div :class="className" :id="id" :style="{height:height,width:width}" ref="myEchart"></div>
    </div>
    <Button @click="fighting" style="margin-top:10px" type="warning" size="large">我也要为祖国加油</Button>
  </div>
</template>

<script>
import echarts from "echarts";
import "../../node_modules/echarts/map/js/world.js";
export default {
  name: "echars",
  props: {
    className: {
      type: String,
      default: "yourClassName"
    },
    id: {
      type: String,
      default: "yourID"
    },
    width: {
      type: String,
      default: "100%"
    },
    height: {
      type: String,
      default: "400px"
    }
  },
  data() {
    return {
      title: "图表",
      placeholder: "用户名/电话",
      find: "2", //1显示新增按钮，2显示导入按钮，若不显示这两个按钮可以写0或者不写值
      chart: null,
      address: ""
    };
  },
  mounted() {
    //初始化
    this.initChart();
    //定位
    // this.location();
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
      this.location();
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
    chinaConfigure() {
      let myChart = echarts.init(this.$refs.myEchart1); //这里是为了获得容器所在位置
      myChart.setOption({
        // 进行相关配置
        backgroundColor: "#F00",
        tooltip: {}, // 鼠标移到图里面的浮动提示框
        dataRange: {
          show: false,
          min: 0,
          max: 1000000,
          text: ["High", "Low"],
          realtime: true,
          calculable: true,
          color: ["orangered"]
        },
        geo: {
          // 这个是重点配置区
          map: "china", // 表示中国地图
          roam: true,
          label: {
            normal: {
              show: true, // 是否显示对应地名
              textStyle: {
                color: "rgba(0,0,0,0.4)"
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
            name: "启动次数", // 浮动框的标题
            type: "map",
            geoIndex: 0,
            data: [
              {
                name: "广东",
                value: 1324
              }
            ] // 这里就是数据，即数组可以单独放在外面也可以直接写
          }
        ]
      });
    },
    //搜索回调
    searchItem(val) {
      console.log(val);
    },
    //新增回调
    addNew(val) {
      console.log(val);
    },
    //导入
    leadingItem(val) {
      console.log(val);
    },
    initChart() {
      this.chart = echarts.init(this.$refs.myEchart);
      window.onresize = echarts.init(this.$refs.myEchart).resize;
      // 把配置和数据放这里
      this.chart.setOption({
        // backgroundColor: "hsl(0, 0%, 96.4%)",
        title: {
          // text: '在线设备分布',
          left: "40%",
          top: "0px",
          textStyle: {
            color: "#fff",
            opacity: 0.7
          }
        },
        dataRange: {
          show: false,
          min: 0,
          max: 1000000,
          text: ["High", "Low"],
          realtime: true,
          calculable: true,
          color: ["red"]
        },
        tooltip: {
          trigger: "item"
        },
        geo: {
          map: "world",
          label: {
            emphasis: {
              show: false
            }
          },
          roam: false,
          silent: true,
          itemStyle: {
            normal: {
              areaColor: "#fff",
              borderColor: "#000"
            },
            emphasis: {
              areaColor: "#f00"
            }
          }
        },
        series: [
          {
            type: "map",
            mapType: "world",
            // zoom: 1.2,
            mapLocation: {
              y: 100
            },
            data: [
              {
                name: "China",
                value: 1
              }
            ],
            symbolSize: 12,
            label: {
              normal: {
                show: false
              },
              emphasis: {
                show: true
              }
            },
            itemStyle: {
              emphasis: {
                borderColor: "#ff0",
                borderWidth: 1
              }
            }
          }
        ]
      });
    }
  }
};
</script>

<style scoped>
.echart {
  padding-top: 10px;
}
</style>
