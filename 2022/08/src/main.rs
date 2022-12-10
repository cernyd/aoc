use std::{io::{Lines, BufReader, BufRead}, fs::File};


#[derive(Debug)]
struct TreeMap {
    trees: Vec<usize>,
    visible: Vec<bool>,
    rows: usize,
    cols: usize
}


impl TreeMap {
    fn new(trees: Vec<usize>, rows: usize, cols: usize) -> TreeMap {
        return TreeMap {
            trees: trees,
            visible: vec![false; rows*cols],
            rows: rows,
            cols: cols
        };
    }

    fn get_index<T>(&self, array: &Vec<T>, row: usize, col: usize) -> T where T: Copy {
        return array[row*self.rows+col];
    }

    fn get_tree(&self, row: usize, col: usize) -> usize {
        return self.get_index(&self.trees, row, col);
    }

    fn get_row(&self, row: usize) -> Vec<usize> {
        let mut r: Vec<usize> = Vec::new();

        for col in 0..self.cols {
            r.push(self.get_tree(row, col));
        }

        return r;
    }

    fn get_col(&self, col: usize) -> Vec<usize> {
        let mut c: Vec<usize> = Vec::new();

        for row in 0..self.rows {
            c.push(self.get_tree(row, col));
        }

        return c;
    }

    fn get_visible(&self, row: usize, col: usize) -> bool {
        return self.get_index(&self.visible, row, col);
    }

    fn set_visible(&mut self, row: usize, col: usize, visible: bool) {
        self.visible[row*self.rows+col] = visible;
    }

    fn total_visible(&self) -> usize {
        return self.visible.iter().map(|val| *val as usize).sum::<usize>();
    }
}


// From day 6
fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let file = File::open(path.as_ref()).expect("Unable to open file");
    let reader = BufReader::new(file);
    return reader.lines();
}


fn load_map<T: AsRef<str>>(path: T) -> TreeMap {
    let mut trees: Vec<usize> = Vec::new();

    let mut rows: usize = 0;
    let mut cols: usize = 0;

    for line in  read_lines(path).map(|line| line.unwrap()) {
        for tree in line.chars().map(|ch| String::from(ch).parse::<usize>().unwrap()) {
            trees.push(tree);
        }

        cols = line.len();
        rows += 1;
    }

    return TreeMap::new(trees, rows, cols);
}


fn main() {
    let mut tree_map = load_map("map.txt");

    println!("--- Left to right rows ---");

    for row in 0..tree_map.rows {
        let mut highest: usize = 0;
        for (col, tree_height) in tree_map.get_row(row).iter().enumerate() {
            check_visible(col, &mut tree_map, row, tree_height, &mut highest);
        }
    }

    println!("--- Right to left rows ---");
    for row in 0..tree_map.rows {
        let mut highest: usize = 0;
        for (col, tree_height) in tree_map.get_row(row).iter().enumerate().rev() {
            check_visible(col, &mut tree_map, row, tree_height, &mut highest);
        }
    }

    println!("--- Top down cols ---");
    for col in 0..tree_map.cols {
        let mut highest = 0;
        for (row, tree_height) in tree_map.get_col(col).iter().enumerate() {
            check_visible(col, &mut tree_map, row, tree_height, &mut highest);
        }
    }

    println!("--- Bottom up cols ---");
    for col in 0..tree_map.cols {
        let mut highest = 0;
        for (row, tree_height) in tree_map.get_col(col).iter().enumerate().rev() {
            check_visible(col, &mut tree_map, row, tree_height, &mut highest);
        }
    }

    println!("--- FINAL VISIBILITY ---");
    print_visibility(&tree_map);

    println!("Total visible: {}", tree_map.total_visible());
}


fn print_visibility(tree_map: &TreeMap) {
    for row in 0..tree_map.rows {
        for col in 0..tree_map.cols {
            if tree_map.get_visible(row, col) {
                print!("X ");
            } else {
                print!("O ");
            }
        }
        println!();
    }
}


fn check_visible(col: usize, tree_map: &mut TreeMap, row: usize, tree_height: &usize, highest: &mut usize) {
    println!("Tree ({row}, {col})");
    // Edge tree check
    if col == 0 || col == tree_map.cols-1 || row == 0 || row == tree_map.rows-1 {
        println!("edge tree");
        tree_map.set_visible(row, col, true);
    }

    // Higher than previous check
    if *tree_height > *highest {
        println!("higher");
        tree_map.set_visible(row, col, true);
        *highest = *tree_height;
    }
}
