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
            console.log(this.finished);
            this.$emit("filter",this.finished, this.sort)
        }
    }


}
</script>