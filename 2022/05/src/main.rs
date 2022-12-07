use std::{self, fs::{File}, io::Lines};
use std::io::{BufRead, BufReader};


enum ReadState {
    /// Pushing lines to `crates`
    CRATES,
    /// Pushing lines to `moves` (move instructions)
    MOVES
}


fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let file = File::open(path.as_ref()).expect(
        format!("Cannot open file '{}'", path.as_ref()).as_str()
    );
    let reader = BufReader::new(file);
    return reader.lines();
}


// Loads lines related to crates to `crates` (up to the empty separating line)
// Loads lines related to crate moves to `moves`
fn load_data(crates: &mut Vec::<String>, moves: &mut Vec::<String>) {
    let lines = read_lines("crates.txt");

    // Simple state machine
    let mut state = ReadState::CRATES;
    for line in lines.map(|line| line.unwrap()) {
        match state {
            // Push to `crates`
            ReadState::CRATES => {
                if line.is_empty() {
                    state = ReadState::MOVES;
                } else {
                    crates.push(line);
                }
            },
            // Push to `moves`
            ReadState::MOVES => {
                moves.push(line);
            }
        };
    }
}


fn parse_crate_line(crate_line: &String, crate_stacks: &mut Vec::<Vec::<char>>) {
    let mut stack_i = 0;

    for (i, ch) in crate_line.chars().enumerate() {
        println!("Index: {i}");
        if i % 4 != 1 { continue; }

        // Push a crate if present
        match ch {
            'A'..='Z' => {
                println!("Push '{ch}' to stack {stack_i}");
                crate_stacks[stack_i].push(ch);
            },
            _ => {
                println!("No value on stack {stack_i}");
            }
        }

        stack_i += 1;
    }
}


// Gets number of stacks based based on crate stack numbering line (1 2 3 ...)
fn get_stack_count(line: &String) -> i32 {
    return str::parse::<i32>(
        line.split(' ').last().unwrap()
    ).unwrap();
}


// Executes a move instruction on crate stacks
fn execute_instruction(instruction: &String, crate_stacks: &mut Vec::<Vec::<char>>) {
    let words: Vec<&str> = instruction.split(" ").collect();

    // Get count of crates to move and source/target stack
    let count = words[1].parse::<usize>().unwrap() - 1;
    let from = words[3].parse::<usize>().unwrap() - 1;
    let to = words[5].parse::<usize>().unwrap() - 1;

    // Execute move
    for _ in 0..=count {
        let cr = crate_stacks[from].pop().unwrap();
        crate_stacks[to].push(cr);
    }
}


// Prints all crate stacks and their values
fn print_crate_stacks(crate_stacks: &Vec::<Vec::<char>>) {
    for (i, crate_stack) in crate_stacks.iter().enumerate() {
        print!("Stack {i}:");
        for cr in crate_stack.iter() {
            print!(" {} ->", cr);
        }
        println!(" END");
    }
}


fn main() {
    // Raw crates lines
    let mut crates: Vec::<String> = Vec::new();
    // Raw moves lines
    let mut moves: Vec::<String> = Vec::new();
    // Crate stacks
    let mut crate_stacks: Vec::<Vec::<char>> = Vec::new();

    // Load raw crates and moves data
    load_data(&mut crates, &mut moves);

    // Get total count of crate stacks
    let stack_count = get_stack_count(crates.last().unwrap());

    // Pops last crates line (only contains crate stack numbers)
    crates.pop();
    // Reverse crate lines to load crates in correct order
    crates.reverse();

    // Initialize empty crate stacks
    for _ in 0..stack_count {
        crate_stacks.push(Vec::<char>::new());
    }

    // Parses and pushes crates to crate stacks
    for (i, crate_line) in crates.iter().enumerate() {
        println!("=== PARSE LINE {i} ===");
        parse_crate_line(&crate_line, &mut crate_stacks);
    }

    println!("=== END OF CRATE PARSING ===");

    // Debug print before moves
    println!("--- BEFORE ---");
    print_crate_stacks(&crate_stacks);

    // Execute all move instructions on stacks
    for instruction in moves.iter() {
        execute_instruction(instruction, &mut crate_stacks);
    }

    // Debug print after moves
    println!("--- AFTER ---");
    print_crate_stacks(&crate_stacks);

    // Prints results
    print!("Result: ");
    for crate_stack in crate_stacks.iter() {
        print!("{}", crate_stack.last().unwrap());
    }
    println!()
}
