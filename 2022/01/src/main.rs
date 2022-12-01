// https://adventofcode.com/2022/day/1
use std::fs::File;
use std::io::{self, BufRead};


fn main() {
    let filename = "calories.txt";
    println!("Using file '{filename}'");

    // Setup file read
    let file = File::open(filename).expect(
        &format!("Failed to open file '{filename}'").to_string()
    );
    let reader = io::BufReader::new(file);

    let mut elf_calories = Vec::<i64>::new();
    if let Ok(lines) = Ok::<std::io::Lines<io::BufReader<File>>, String>(reader.lines()) {
        let mut current_calories: i64 = 0;
        // Iterate over calorie lines
        for line in lines {
            if let Ok(line_value) = line {
                // Compare current max with new value, zero current calories
                if line_value.is_empty() {
                    elf_calories.push(current_calories);
                    current_calories = 0;
                // Add calories
                } else {
                    current_calories += line_value.parse::<i64>().unwrap();
                }
            }
        }
    }

    // Get top 3 results
    let mut top_3 = Vec::<i64>::new();
    for _ in 0..3 {
        top_3.push(pop_max(&mut elf_calories));
    }

    let max_calories = top_3[0];
    println!("Maximum elf calories: {max_calories} calories");
    let top_3_sum = top_3.iter().sum::<i64>();
    println!("Top 3 elf calories: {top_3_sum}")
}


// Finds and removes the maximum value from the vector
fn pop_max(vector: &mut Vec<i64>) -> i64 {
    let mut max_i: usize = 0;
    let mut max: i64 = 0;

    for (i, value) in vector.iter().enumerate() {
        if value > &max {
            max = *value;
            max_i = i;
        }
    }

    vector.remove(max_i);
    return max;
}
