rule scanf_rule {
    meta:
        name = "scanf"
    strings:
        $scanf_string = "scanf"
        $_string = "scanf_s"
        $2_string = "sscanf"
    condition:
        $scanf_string and (not $_string) and (not $2_string)
}

