rule gets_rule {
    meta:
        name = "gets"
    strings:
        $gets_string = "gets"
        $fgets_string = "fgets"
    condition:
        $gets_string and (not $fgets_string)
}