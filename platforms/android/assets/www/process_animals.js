function process_animal()
{
    var animal_data = JSON.parse(window.localStorage.getItem("animals"));
    
    var animal_array = Object.values(animal_data);
    var parsed_array =[];
    for(var i =0; i < animal_array.length;i++)
        {
            var temp_array = Object.values(animal_array[i]);        
            if(temp_array.length == 8)
                {
                    if(parsed_array.indexOf(temp_array[1] == -1 | parsed_array.length ==0))
                        {
                             parsed_array.push(temp_array[1]);
                        }

                }
        }
    var select_tag = document.getElementById("animal");
    var option;
    option = document.createElement("option");
    option.text = "--Select an Animal--";
    select_tag.add(option);
    
    for(var i =0; i < parsed_array.length;i++)
        { 
            option = document.createElement("option");
            option.text = parsed_array[i];
            select_tag.add(option);
        }
   
}
function populate_select()
{
    var animal_data = JSON.parse(window.localStorage.getItem("animals"));
    var animal_array = Object.values(animal_data);
    var choice = document.getElementById("animal").value;
    
    var parsed_array =[]
    for(var i =0; i < animal_array.length;i++)
        {
            var temp_array = Object.values(animal_array[i]);
        
            if(temp_array.length == 8)
                {
                    if(temp_array[1] == choice)
                        {
                            $("#trackingNum").val(temp_array[7]);   
                        }
                }
        }
}
function back()
{
    window.location.replace("home.html");
}