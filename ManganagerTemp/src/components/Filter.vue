<template>
    <div>
        Display :
        <input type="checkbox" id="isFinished" @click="finished = !finished; send_event()"/>
        <label>Finished</label>

        Sort by:

        <input type="checkbox" id="date" @click="sort = 'date';send_event()"/>
        <label>Date</label>

        <input type="checkbox" id="remaining" @click="sort = 'remaining';send_event()"/>
        <label>Remaining chapters</label>

        <input type="checkbox" id="site" @click="sort = 'site';send_event()"/>
        <label>Sites</label>
    </div>
</template>

<script>


export default{
    name: "Filter",
    data(){
        return {
            finished:false,
            sort: "date",
        }
    },
    methods:{
        send_event(){
            this.$emit("filter",this.finished, this.sort)
        }
    }


}
</script>