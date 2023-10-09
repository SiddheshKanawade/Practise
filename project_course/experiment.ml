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
  nst_nested: int list;
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

let block_elements_to_add = [
  element1; 
  element2;
]

let nested_blocks_with_elements =
  List.fold_left (fun nested_blocks element -> add_nested_element nested_blocks element) nested_blocks block_elements_to_add

let worst_case_time_of_block nested_block nested_blocks_with_elements task_number block_number = 
  if nested_block.nst_wcrt > 0.0 then nested_block.nst_wcrt
  else
    begin
      print_endline "Need to execute";
      let cij = nested_block.nst_wcet in
      (let l = [] in)
      let prio = nested_block.nst_priority in
      print_endline ("Currently with block " ^ nested_block.nst_task_type);
      (Iterate over the list nested_blocks_with_elements)
      let aggregated_nested_blocks = nested_blocks_with_elements.nst_elements in
      let rec get_individual_nested_block_list aggregated_nested_block_list prio nested_block l =
        match aggregated_nested_block_list with
        | [] -> l (* Base case: an empty task_list, return L *)
        | nested_block :: rest ->
            print_endline ("Currently with block " ^ nested_block.nst_task_type);
            if nested_block.nst_priority > prio then 
              print_endline ("priority less than mentioned");
            get_individual_nested_block_list rest prio nested_block l;
      in 
      get_individual_nested_block_list aggregated_nested_blocks prio nested_block [];
      nested_block.nst_wcrt
    end 
let ans:float = worst_case_time_of_block element1 nested_blocks_with_elements 1 2

