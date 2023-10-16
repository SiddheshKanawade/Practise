(* This is an OCaml editor.
Enter your program here and send it to the toplevel using the "Eval code" button or [Ctrl-e]. *)

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

let create_nested_block_element nst_key nst_task_type nst_lock_name nst_wcet nst_wcrt nst_time_period nst_priority nst_nested =
  { nst_key; nst_task_type; nst_lock_name; nst_wcet; nst_wcrt; nst_time_period; nst_priority; nst_nested }

let create_nested_block () =
  { nst_elements = [] }


let add_nested_element block nst_element =
  { block with nst_elements = nst_element :: block.nst_elements }
let nested_blocks = create_nested_block ()

let element1 = create_nested_block_element 0 "TaskMainDisplayTask" "DrivingControlResource" 0.411 0.0 250 10 [1]

let element2 = create_nested_block_element 1 "DrivingControlResource" "DrivingControlResource" 0.22 0.0 250 13 []
    
let element3 = create_nested_block_element 0 "TaskMainDisplayTask" "DrivingControlResource1" 0.411 0.0 250 10 [1]
    
let element4 = create_nested_block_element 0 "TaskMainDisplayTask" "DrivingControlResource2" 0.411 0.0 250 10 [1]

let block_elements_to_add = [
  element1; 
  element2;
  element3;
  element4;
]

let nested_blocks_with_elements =
  List.fold_left (fun nested_blocks element -> add_nested_element nested_blocks element) nested_blocks block_elements_to_add

let worst_case_time_of_block nested_block grouped_elements task_number block_number = 
  if nested_block.nst_wcrt > 0.0 then nested_block.nst_wcrt
  else
    begin
      print_endline "Iterating over allblocklist";
      let cij = nested_block.nst_wcet in
      let lock_name_list = [] in (*analogous to L*)
      (*let l = [] in*)
      let prio = nested_block.nst_priority in
      List.iter(fun task_group ->
          Printf.printf "Task Type: %s\n" (List.hd task_group).nst_task_type;
          if (List.hd task_group).nst_priority > prio then
            List.iter (fun element ->
                Printf.printf "Key: %d, Lock Name: %s Task Type: %s\n" element.nst_key element.nst_lock_name element.nst_task_type;
                if element.nst_lock_name==nested_block.nst_lock_name then
                  List.iter(fun nst_index ->
                      Printf.printf "Index: %d\n" nst_index;
                      let short_live_list=[element.nst_lock_name] in
                      (*Append lock_name_list and short_live_list*)
                      let new_list=lock_name_list@short_live_list;
                    ) element.nst_nested
              ) task_group
        ) grouped_elements;
        
      nested_block.nst_wcrt
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
      Printf.printf "Task Type: %s\n" (List.hd group).nst_task_type;
      List.iter (fun element ->
          Printf.printf "Key: %d, Lock Name: %s\n" element.nst_key element.nst_lock_name; 
          List.iter(fun index->
              Printf.printf "Index: %d\n" index;
            ) element.nst_nested
        ) group
    ) grouped_elements

let ans:float = worst_case_time_of_block element1 grouped_elements 1 2

