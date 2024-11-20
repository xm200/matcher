rule strcat_rule {
    meta:
        name = "strcat"
    strings:
        $s = "strcat("
    condition:
        $s
}
