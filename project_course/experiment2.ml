(* This is an OCaml editor.
Enter your program here and send it to the toplevel using the "Eval code" button or [Ctrl-e]. *)
open Stdlib


type nested_block_element = { 
  nst_key: int; 
  nst_task_type: string; 
  nst_lock_name: string; 
  nst_wcet: float;
  nst_wcrt: float;
  nst_time_period: int;
  nst_priority: int;
  nst_nested: int list; (*Key goes into this*)
}


type nested_block = {
  nst_elements: nested_block_element list;
}

let lock_name_list = ref [] ;;

let epsilon = 0.001 ;;

let create_nested_block_element nst_key nst_task_type nst_lock_name nst_wcet nst_wcrt nst_time_period nst_priority nst_nested =
  { nst_key; nst_task_type; nst_lock_name; nst_wcet; nst_wcrt; nst_time_period; nst_priority; nst_nested }

let create_nested_block () =
  { nst_elements = [] }


let add_nested_element block nst_element =
  { block with nst_elements = nst_element :: block.nst_elements }
let nested_blocks = create_nested_block ()

(*Create block list properly after verifying*)
(*Task 1*)
let element1 = create_nested_block_element 0 "TaskMainDisplayTask" "TaskMainDisplayTask" 0.411 0.0 250 10 [1]

let element2 = create_nested_block_element 1 "TaskMainDisplayTask" "DrivingControlResource" 0.22 0.0 250 10 [] 
    
    (*Task 2*)
let element3 = create_nested_block_element 0 "TaskMainColorSensorTask" "TaskMainColorSensorTask" 0.068 0.0 100 2 [1;2]
    
let element4 = create_nested_block_element 1 "TaskMainColorSensorTask" "DrivingControlResource" 0.028 0.0 100 2 []
    
let element5 = create_nested_block_element 2 "TaskMainColorSensorTask" "DrivingControlResource" 0.02 0.0 100 2 []
    
(*Task 3*)
let element6 = create_nested_block_element 0 "TaskMainSonarSensorTask" "TaskMainSonarSensorTask" 0.114 0.0 100 5 [1;2;3;4;5;6;7;8]
    
let element7 = create_nested_block_element 1 "TaskMainSonarSensorTask" "DrivingControlResource" 0.019 0.0 100 5 []
    
let element8 = create_nested_block_element 2 "TaskMainSonarSensorTask" "DrivingControlResource" 0.018 0.0 100 5 []
    
let element9 = create_nested_block_element 3 "TaskMainSonarSensorTask" "DrivingControlResource" 0.01 0.0 100 5 []
    
let element10 = create_nested_block_element 4 "TaskMainSonarSensorTask" "DrivingControlResource" 0.018 0.0 100 5 []
    
let element11 = create_nested_block_element 5 "TaskMainSonarSensorTask" "DrivingControlResource" 0.012 0.0 100 5 []
    
let element12 = create_nested_block_element 6 "TaskMainSonarSensorTask" "DrivingControlResource" 0.019 0.0 100 5 []
    
let element13 = create_nested_block_element 7 "TaskMainSonarSensorTask" "DrivingControlResource" 0.022 0.0 100 5 []
    
let element14 = create_nested_block_element 8 "TaskMainSonarSensorTask" "DrivingControlResource" 0.019 0.0 100 5 []
    
    (*Task 4*)
let element15 = create_nested_block_element 0 "TaskMainMotorControlTask" "TaskMainMotorControlTask" 0.074 0.0 50 1 [1]
    
let element16 = create_nested_block_element 0 "TaskMainMotorControlTask" "DrivingControlResource" 0.071 0.0 50 1 []


let block_elements_to_add = [
  element1; 
  element2;
  element3;
  element4;
  element5;
  element6;
  element7;
  element8;
  element9;
  element10;
  element11;
  element12;
  element13;
  element14;
  element15;
  element16;
]

let nested_blocks_with_elements =
  List.fold_left (fun nested_blocks element -> add_nested_element nested_blocks element) nested_blocks block_elements_to_add

let rec find_value_at_index arr task_number block_number =
  match arr with
  | [] -> failwith "Array index out of bounds"
  | row :: remaining_rows ->
      if task_number = 0 then
        match row with
        | [] -> failwith "Array index out of bounds"
        | value :: _ when block_number = 0 -> value
        | _ :: rest_of_row -> find_value_at_index (rest_of_row :: remaining_rows) 0 (block_number - 1)
      else
        find_value_at_index remaining_rows (task_number - 1) block_number
;;    

let equalsf x y epsilon =
  abs_float (x -. y) < epsilon;;

let isSat_eqn2 init_li current_li high_tasks = 
  let new_li = ref init_li in
  List.iter(fun task->
      let float_timeperiod = float_of_int task.nst_time_period in
      let task_wcet = task.nst_wcet in 
      let calculated_val = current_li /. float_timeperiod *. task_wcet in
      new_li := !new_li +. ceil calculated_val
    )high_tasks;
  (*Figureout how epsilon is passing into the function, as its declared globally?*)
  let result = equalsf current_li !new_li epsilon in
  result
;;

let compute_Lilk current_li prev_li high_tasks = 
  let new_li = ref current_li in
  List.iter(fun task ->
      let float_timeperiod = float_of_int task.nst_time_period in
      let task_wcet = task.nst_wcet in
      let calculated_val1 = current_li /. float_timeperiod *. task_wcet in
      let calculated_val2 = prev_li /. float_timeperiod *. task_wcet in
      new_li := !new_li +. ceil calculated_val1;
      new_li := !new_li -. ceil calculated_val2;
    )high_tasks;
  !new_li
;;


let rec loop init_li current_li prev_li nested_block grouped_elements task_number = 
  let prio=nested_block.nst_priority in 
  let tasklist=List.map (fun task -> List.hd task) grouped_elements in
  let high_tasks = List.filter (fun x -> x.nst_priority > prio) tasklist in
  (*Define isSat_eq2 here*)
  if not (isSat_eqn2 init_li current_li high_tasks) && current_li < float_of_int nested_block.nst_time_period then
    begin
      let new_lilk = compute_Lilk current_li prev_li high_tasks in
      loop init_li new_lilk current_li nested_block grouped_elements task_number
    end
  else if current_li >= float_of_int nested_block.nst_time_period then
    begin
      Printf.printf "Unschedulable block - %s" nested_block.nst_lock_name;
      -1.0
    end 
  else 
    current_li
;;

let rec worst_case_time_of_block nested_block grouped_elements task_number block_number = 
  if nested_block.nst_wcrt > 0.0 then nested_block.nst_wcrt
  else
    begin
      print_endline "Iterating over allblocklist";
      let cij = nested_block.nst_wcet in 
      (*let l = [] in*)
      let prio = nested_block.nst_priority in
      List.iter(fun task_group ->
          Printf.printf "Task Type: %s\n" (List.hd task_group).nst_task_type;
          if (List.hd task_group).nst_priority > prio then
            List.iter (fun element ->
                Printf.printf "Key: %d, Lock Name: %s Task Type: %s\n" element.nst_key element.nst_lock_name element.nst_task_type;
                if element.nst_lock_name==nested_block.nst_lock_name then
                  List.iter(fun nst_index ->
                      Printf.printf "entered";
                      lock_name_list := !lock_name_list @ [element.nst_lock_name]
                    ) element.nst_nested
              ) task_group
        ) grouped_elements;
      
      
      List.iter(fun nst_index ->
          let lock_element = find_value_at_index grouped_elements task_number nst_index in
          lock_name_list := !lock_name_list @ [lock_element.nst_lock_name]
        )nested_block.nst_nested;
      
      let waiting_time= ref 0.0 in
      
      List.iter (fun lock_name ->
          Printf.printf "LockName: %s\n" lock_name; 
          let time = ref 0.0 in
          List.iteri(fun index_task task_group->
              if (List.hd task_group).nst_priority < prio then
                List.iteri(fun index_element element->
                    if element.nst_lock_name==lock_name then 
                      let calculated_time=worst_case_time_of_block element grouped_elements index_task index_element in
                      if calculated_time > !time then
                        time := calculated_time
                  )task_group;
              waiting_time := !waiting_time +. !time
            ) grouped_elements 
        )!lock_name_list ;
      let new_cij = cij +. !waiting_time in
      let wcrt = loop new_cij new_cij 0.0 nested_block grouped_elements task_number in
      (*Set given block wcrt as calculated wcrt*)
      let grouped_elements = List.mapi(fun task_index task_group ->
          if task_index = task_number then
            begin
              List.mapi(fun nested_block_index element ->
                  if nested_block_index=block_number then
                    { element with nst_wcrt = wcrt }
                  else element
                )task_group
            end
          else task_group
        )grouped_elements in
      wcrt
    end 
    
(*Generating all block list*)
(*Locks for an task are added together into a list*)
(*All block list is stored in hashmap, where every key denotes the name of task*)
let group_elements_by_task_type elements =
  let task_type_map = Hashtbl.create 10 in
  List.iter (fun element ->
      let task_type = element.nst_task_type in
      let current_list = Hashtbl.find_opt task_type_map task_type in
      match current_list with
      | Some(lst) -> Hashtbl.replace task_type_map task_type (element :: lst)
      | None -> Hashtbl.add task_type_map task_type [element]
    ) elements;
  Hashtbl.fold (fun _ elements acc -> elements :: acc) task_type_map []
    
    
let grouped_elements = group_elements_by_task_type nested_blocks_with_elements.nst_elements
(*Print the all block list*)
let () =
  List.iter (fun group ->
      Printf.printf "\n";
      List.iter (fun element ->
          Printf.printf "Key: %d, Lock Name: %s\n" element.nst_key element.nst_lock_name; 
          List.iter(fun index->
              Printf.printf "Index: %d\n" index;
            ) element.nst_nested
        ) group
    ) grouped_elements

let ans:float = worst_case_time_of_block element1 grouped_elements 1 2

