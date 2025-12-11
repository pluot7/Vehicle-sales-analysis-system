<template>
  <div id="bottomRight">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span>
          <icon name="chart-area" class="text-icon"></icon>
        </span>
        <div class="d-flex">
          <span class=" text mx-2">汽车排行总榜</span>
          <div class="decoration2">
            <dv-decoration-2 :reverse="true" style="width:5px;height:6rem;" />
          </div>
        </div>
      </div>
      <div class="row_list">
        <ul class="car_rank" style="width: 100%;overflow: auto;height: 420px">
          <li style="font-size: 23px">
            <div>销售排名</div>
<!--            <div>图片</div>-->
            <div>汽车信息</div>
            <div>销售价格</div>
            <div>销售趋势</div>
            <div>保修时间</div>
            <div>上市时间</div>
          </li>
          <li v-for="car in carData" v-bind:key="car.rank">
            <div>{{ car.rank }}</div>
<!--            <div class="list_img"><img :src="car.carImag " style="height: 100%;width: 1000%" alt=""></div>-->
            <div class="list_info">
              <p>{{ car.carName }}</p>
            <p>{{ car.manufacturer }}/{{ car.brand }}</p>
            </div>

            <div>{{ car.price }}</div>
            <div>{{ car.saleVolume }}辆</div>
            <div>{{ car.insure }}</div>
            <div>{{ car.marketTime}}</div>

          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
// import BottomRightChart from "@/components/echart/bottom/bottomRightChart";
export default {
  data(){
    return{
      carData:''
    }
  },
  components: {
    // BottomRightChart
  },
  async mounted(){
    const res=await this.$http.get('myApp/bottomRight')
    this.carData=res.data.carData
    // console.log(this.carData)
  }

};
</script>

<style lang="scss" class>
$box-height: 520px;
$box-width: 100%;
#bottomRight {
  padding: 14px 16px;
  height: $box-height;
  width: $box-width;
  border-radius: 5px;
  .bg-color-black {
    height: $box-height - 30px;
    border-radius: 10px;
  }
  .text {
    color: #c3cbde;
  }
  //下滑线动态
  .decoration2 {
    position: absolute;
    right: 0.125rem;
  }
  .chart-box {
    margin-top: 16px;
    width: 170px;
    height: 170px;
    .active-ring-name {
      padding-top: 10px;
    }
  }
}
//列表
  .row_list{
    list-style: none;
    .car_rank::-webkit-scrollbar {
      display: none;
    }
    .car_rank li{
      display: grid;
      -ms-grid-columns:100px 150px 108px 120px 120px 110px 100px;
      grid-template-columns: 100px 150px 180px 120px 120px 110px 100px;
      margin-left: 23px;
      cursor: pointer;
      text-align: center;
      line-height: 30px;
    }
  }
</style>